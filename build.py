# todo:
#-get rid of search bar
#- get rid of made with heart
#- make photos smaller


#import statements -----------
import datetime
import glob
import os
from jinja2 import Template

#lists---------------
list_of_pages = []



#functions--------------
def main():
    create_page_list()
   # create_menu(list_of_pages)
    create_full_base()
    #assemble each page 
    for page in list_of_pages:
        title= page["title"]
        filename= page["filename"]
        output= page["output"]
        #add in filename and output so can use them
        base= assign_base(title)
        assemble_page(title, base, filename, output)           

        
     

#build the list of pages automatically
def create_page_list():
    all_html_files = glob.glob("content/*.html")
    for page in all_html_files:
        file_path = page
        file_name = os.path.basename(file_path)
        name_only, extension = os.path.splitext(file_name)
        file_dict = {
            "filename": page,
            "output": "docs/"+ name_only + ".html",
            "title": name_only,
        }
        list_of_pages.append(file_dict)
    for html_page in list_of_pages: #just for my use. will delete
        print(html_page)    

#generate a menu from the list_of_pages 
def create_menu(pages):
    header_footer = open("templates/headerfooter.html").read()
    menu = ""
    #generate menu link for each page
    for page in pages:
        title = page["title"]
        caps_title=title.capitalize()
        if title == "index":
            caps_title = "Home"
        menu_item = '<li class="nav-item">\n\t<a class="nav-link" href="'+ title + '.html">' +caps_title+'</a>\n</li>'
        menu = menu + menu_item
    #place menu in headerfooter template
    #make it a function that gets passed a variable!!!
    #what if i do variables (template, placeholder, content) and then do a seperate render for each insertion
    template = Template(header_footer)
    menu_inserted = template.render(
        menu_items= menu,
    )  
    open("templates/headerfooter.html", "w+").write(menu_inserted)
    #place menu in home content
    home_content = open("content/index.html").read()
    template = Template(home_content)
    menu_inserted = template.render(
        menu_items = menu,
    )  
    open("content/index.html", "w+").write(menu_inserted)

# Create full base with header and footer    
def create_full_base():
    #open basic base
    base_template = open("templates/base.html").read()
    # Read in the header and footer
    header_footer = open("templates/headerfooter.html").read()
    # Add header and footer to basic base
    template = Template(base_template) ## use templating function?
    full_base=template.render(
        header_footer=header_footer,
    )  
    open("templates/fullbase.html", "w+").write(full_base)     
       
# Chooses correct base for each page
def assign_base(page_name):
    base = None
    #index gets basic base, others get full base    
    if page_name == "index":
        base = open("templates/base.html").read()
    else:
        base = open("templates/fullbase.html").read()
    return base
       
            
#replace placeholder in each page with the page's content, title, year
def assemble_page(page_name, page_template, filename, output):
    # Define content, title, and year
    content = open(filename).read()
    if page_name == "index":
        title = "Home"
        #index = open(filename).read()
        #page_content = None
    else:
        title= page_name.capitalize()
        #page_content = open(filename).read()
        #index = None
    now = datetime.datetime.now()
    year=str(now.year)
    print(page_name, filename, output)
    # put those into template
    #write a dictionary for the rendering to go through?
    
    #templating(page_template, 'content', page_content, index, title, year, output)
    

#perform templating
#def templating (open_page, placeholder, page_content, page_index, page_title, page_year, output_page): #put these in a list?
    template = Template(page_template)
    finished_page=template.render(
        content = content, #this has to say content on the left side. not "content"
        #this is really inelegant
        title = title,
        year = year,
    )  
    open(output, "w+").write(finished_page)    

        

#run--------------    
if __name__ == "__main__":
    main()
    
