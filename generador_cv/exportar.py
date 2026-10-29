import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def office():
    binary = os.environ.get("CV_SOFFICE") or shutil.which("soffice") or shutil.which("libreoffice")
    if not binary:
        for p in [r"C:\Program Files\LibreOffice\program\soffice.exe", "/Applications/LibreOffice.app/Contents/MacOS/soffice"]:
            if Path(p).is_file():
                binary = p
                break
    if not binary and os.name == "nt":
        import winreg
        try:
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\winword.exe")
            val = winreg.QueryValue(k, None)
            if val and Path(val).is_file():
                return val
        except Exception:
            pass
    if not binary:
        raise RuntimeError("Falta LibreOffice o Microsoft Word. No se puede exportar.")
    return binary


def convert(paths, out):
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = office()
    if target.lower().endswith("winword.exe"):
        ps_lines = [
            "$word = New-Object -ComObject Word.Application",
            "$word.Visible = $false",
            "$word.DisplayAlerts = [Microsoft.Office.Interop.Word.WdAlertLevel]::wdAlertsNone",
            "try {"
        ]
        for p in paths:
            src = Path(p).resolve()
            dst = out / (src.stem + ".pdf")
            ps_lines.append("    $doc = $word.Documents.Open('{}', $false, $true)".format(str(src).replace("'","''")))
            ps_lines.append("    $doc.SaveAs([ref]'{}', [ref]17)".format(str(dst).replace("'","''")))
            ps_lines.append("    $doc.Close($false)")
        ps_lines.extend([
            "} finally {",
            "    $word.Quit()",
            "    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null",
            "}"
        ])
        script = "\n".join(ps_lines)
        result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], capture_output=True, text=True, timeout=180)
        if result.returncode or any(not (out / (Path(p).stem + ".pdf")).is_file() for p in paths):
            raise RuntimeError("Word no exportó todos los documentos: " + result.stdout[-1500:] + result.stderr[-1500:])
        return [out / (Path(p).stem + ".pdf") for p in paths]

    with tempfile.TemporaryDirectory(prefix="cv-office-") as profile:
        result = subprocess.run([target, "-env:UserInstallation=" + Path(profile).as_uri(),
            "--headless", "--convert-to", "pdf:writer_pdf_Export", "--outdir", str(out),
            *[str(Path(p).resolve()) for p in paths]], capture_output=True, text=True, timeout=180)
        if result.returncode or any(not (out / (Path(p).stem + ".pdf")).is_file() for p in paths):
            raise RuntimeError("LibreOffice no exportó todos los documentos: " + result.stdout[-1500:] + result.stderr[-1500:])
    return [out / (Path(p).stem + ".pdf") for p in paths]
