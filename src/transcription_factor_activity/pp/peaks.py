from typing import Union
import tempfile
import os
import shutil


def call_peaks(
    fragpaths: Union[str, list],
    macs2_path: str = None,
    outdir: str = tempfile.gettempdir(),
    broad: bool = False,
    format: str = "BED",
    effective_genome_size: int = 2.7e9,
    pval_thresh: float = 0.01,
    extsize: int = 200,
    shift: float = None,
    kwargs: dict = None,
):
    """Run relaxed peak calling on pseudo bulk files.

    Parameters
    ----------
        fragpaths : Union[str, list]
        Path to fragment files. If multiple paths are given, they are collapsed to a single space-separated string.

    Returns
    -------
    None
    """
    # ENCODE: -B --SPMR --keep-dup all --call-summits

    # find macs2
    macs2_path = macs2_path or shutil.which("macs2")

    if macs2_path is None:
        raise ValueError("macs2 not found in PATH")

    # check if fragpaths is a list
    if isinstance(fragpaths, str):
        fragpaths = [fragpaths]

    # if list of paths given, collapse to a single space-separated string
    fragpaths = " ".join(fragpaths)

    # compute shift
    if shift is None:
        shift = -int(round(float(extsize) / 2.0))

    broadstr = "--broad" if broad else ""
    nomod_str = f"--nomodel --extsize {extsize} --shift {shift}" if format == "BED" else ""

    args = ""
    for key, value in kwargs.items():
        if isinstance(value, bool):
            if value:
                args += f"-{key} "
        else:
            args += f"-{key} {value} "
    cmd = f"{macs2_path} callpeak -t {fragpaths} -f {format} -g {effective_genome_size} -p {pval_thresh} {broadstr} {nomod_str} -n {outdir} {args}"

    print(cmd)
    # run cmd
    os.system(cmd)
    return
