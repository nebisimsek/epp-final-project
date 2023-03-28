import pytask
from epp_final_project.config import BLD, PAPER_DIR


@pytask.mark.latex(
    script=PAPER_DIR / "epp_final_project.tex",
    document=BLD / "latex" / "epp_final_project.pdf",
)
def task_compile_latex_document():
    """Compile the document specified in the latex decorator."""
