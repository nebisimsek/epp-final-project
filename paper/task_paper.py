import pytask
from epp_final_project.config import BLD, PAPER_DIR


@pytask.mark.persist
@pytask.mark.latex(
    script=PAPER_DIR / "epp_final_project.tex",
    document=BLD / "latex" / "epp_final_project.pdf",
)
def task_compile_latex_document():
    pass


# for document in documents:

#     @pytask.mark.latex(
#         ),
#     @pytask.mark.task(id=document)
#     def task_compile_document():
#         """Compile the document specified in the latex decorator."""


#     @pytask.mark.task(id=document, kwargs=kwargs)
#     def task_copy_to_root(depends_on, produces):
#         """Copy a document to the root directory for easier retrieval."""
