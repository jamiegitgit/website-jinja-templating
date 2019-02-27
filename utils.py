# todo:
#- make photos smaller
#-change jinja file to make a class for when I'm on that page. then css it


#import statements -----------
import datetime
import glob
import os
from jinja2 import Template

#lists---------------
list_of_pages = []


#functions--------------
def main():
    create_list_of_pages()
    create_interior_files()
    #assemble each page 
    for page in list_of_pages:
        assemble_page(page["title"], page["stage"], page["output"])               

#build the list of pages automatically
def create_list_of_pages():
    all_html_files = glob.glob("content/*.html")
    for page in all_html_files:
        print(page) #delete later
        file_name = os.path.basename(page)
        name_only, extension = os.path.splitext(file_name)
        file_dict = {
            "title": name_only,
            "doc_name":name_only + ".html",
            "input": page,
            "stage": "interior/"+ name_only+".html",
            "output": "docs/"+ name_only + ".html",
        }
        if page == "content/index.html":
            file_dict["title"]="Home"
        list_of_pages.append(file_dict)
    for html_page in list_of_pages: #just for my use. will delete
        print(html_page)    

#put content inside header template, but just copy index over
def create_interior_files():
    for page in list_of_pages:
        print(page["title"], page["input"], page["stage"]) #delete
        # copy index.html from contents to interior
        page_content=open(page["input"]).read()
        if page["title"] == "Home":
            interior_file=page_content
        # sandwich all other pages between header and footer
        else:
            header_footer=open("templates/headerfooter.html").read()
            template = Template(header_footer)
            interior_file = template.render(
                content=page_content,
                #place jinja code to create menu
                menu=menu_jinja(),
                year= "{{year}}",
            )
        open(page["stage"], "w+").write(interior_file)

# import jinja code to make menu
def menu_jinja():
    make_menu= open("templates/menucode.html.j2").read()
    return make_menu

       
            
#replace placeholder in each page with the page's content, title, year
def assemble_page(page_name, interior_file, output):
    #add menu and date to interior files
    interior= open(interior_file).read()
    now = datetime.datetime.now()
    year=str(now.year)
    template=Template(interior)
    templated_interior=template.render(
        pages=list_of_pages, 
        year= year,
    )
    # put interior files in base
    base= open("templates/base.html").read()
    template = Template(base)
    finished_page=template.render(
        content = templated_interior,
        title = page_name,
    )  
    open(output, "w+").write(finished_page)    

        


    
