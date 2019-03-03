
# import statements -----------
import datetime
import glob
import os
from jinja2 import Template

# lists---------------
list_of_pages = []


# functions--------------
def build():
    main()


def main():
    create_list_of_pages()
    create_interior_files()
    # assemble each page
    for page in list_of_pages:
        assemble_page(page["title"], page["stage"], page["output"])


# build the list of pages automatically
def create_list_of_pages():
    all_html_files = glob.glob("content/*.html")
    for page in all_html_files:
        file_name = os.path.basename(page)
        name_only, extension = os.path.splitext(file_name)
        file_dict = {
            "title": name_only,
            "doc_name": name_only + ".html",
            "input": page,
            "stage": "interior/" + name_only + ".html",
            "output": "docs/" + name_only + ".html",
        }
        if page == "content/index.html":
            file_dict["title"] = "Home"
        list_of_pages.append(file_dict)


# put content inside header template, but just copy index over
def create_interior_files():
    for page in list_of_pages:
        # copy index.html from contents to interior
        page_content = open(page["input"]).read()
        if page["title"] == "Home":
            interior_file = page_content
        # template all other pages between header and footer
        else:
            header_footer = open("templates/headerfooter.html").read()
            template = Template(header_footer)
            interior_file = template.render(
                content=page_content,
                year="{{year}}",
                menu="{{menu}}",
            )
        open(page["stage"], "w+").write(interior_file)


# import jinja code to make menu
def menu_jinja():
    make_menu = open("templates/menucode.html.j2").read()
    return make_menu


# replace placeholders in each page with the content, title, year, menu jinja code
def assemble_page(page_name, interior_file, output):
    # add menu code and date to interior files
    interior = open(interior_file).read()
    now = datetime.datetime.now()
    year = str(now.year)
    template = Template(interior)
    templated_interior = template.render(
        year=year,
        # place jinja code to create menu
        menu=menu_jinja(),
    )
    # autogenerate menu
    template = Template(templated_interior)
    templated_interior = template.render(
        pages=list_of_pages,
        page_name=page_name,
    )
    # put interior files in base,
    if page_name == "Home":
        page_name = "index"
    base = open("templates/base.html").read()
    template = Template(base)
    finished_page = template.render(
        content=templated_interior,
        title=page_name,
    )
    open(output, "w+").write(finished_page)


def new():
    blank_content = '''
        <div>
            <p> Insert content here </p>
        </div>'''
    open("content/new.html", "w+").write(blank_content)
