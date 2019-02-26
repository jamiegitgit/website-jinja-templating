
#import statements -----------
import datetime
import glob
import os
from jinja2 import Template

#lists---------------
list_of_pages = []



#functions--------------
def main():
    jinja_test()
    create_page_list()
    create_menu(list_of_pages)
    create_full_base()
    #assemble each page 
    for page in list_of_pages:
        title= page["title"]
        filename= page["filename"]
        output= page["output"]
        #add in filename and output so can use them
        base= assign_base(title)
        assemble_page(title, base, filename, output)           
        #page_title (title, output)
        
     

#trying to build the list automatically
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
    print(list_of_pages)    

#generate a menu from the list_of_pages 
#later step
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
    #place menu in headerfooter template # can jinja this too 
# cAN I COMBINE THESE TWO IN the if statement so i only render once? but need if statement for complete menu. maybe for loop and then an if statement to define what goes in Template(!!!)
    #make it a function that gets passed a variable!!!
    #what if i do variables (template, placeholder, content) and then do a seperate render for each insertion
    # is there a way to just do one render? i think i need a diff render for each file. what if i try to replace a placeholder that doesn't exist?
    template = Template(header_footer)
    menu_inserted = template.render(
        menu_items= menu,
    )  
    #menu_inserted = header_footer.replace("{{menu items}}", menu)
    open("templates/headerfooter.html", "w+").write(menu_inserted)
    #place menu in home content
    home_content = open("content/index.html").read()
    template = Template(home_content)
    menu_inserted = template.render(
        menu_items = menu,
    )  
    #menu_inserted = home_content.replace("{{menu items}}", menu)
    open("content/index.html", "w+").write(menu_inserted)

# Create full base with header and footer    
def create_full_base():
    #open basic base
    base_template = open("templates/base.html").read()
    # Read in the header and footer
    header_footer = open("templates/headerfooter.html").read()
    # Add header and footer to basic base
    #full_base = base_template.replace("{{content}}", header_footer) #jinja it!
    template = Template(base_template)
    full_base=template.render(
        content=header_footer,
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
    
#this is where i am
#     
def jinja_test():
    from jinja2 import Template
    index_html = open("content/index.html").read()
    template_html = open("templates/base.html").read()
    template = Template(template_html)
    test= template.render(
        title="Homepage",
        content=index_html,
        basic="Party",
    )
    open("docs/test.html", "w+").write(test)   
            
#replace placeholder in each page with the page's content
def assemble_page(page_name, page_template, filename, output):
    # Open the content of each HTML page
    content = open(filename).read()
    # place content in template #this will be replaced by jinja
    #finished_page = page_template.replace("{{content}}", content)
   # open(output, "w+").write(finished_page)
    if page_name == "index":
        title = "Home"
    else:
        title= page_name.capitalize()
    now = datetime.datetime.now()
    year=str(now.year)
    template = Template(page_template)
    finished_page=template.render(
        content=content,
        title=title,
        year=year,
    )   #i need to write the output
    open(output, "w+").write(finished_page)
    #open('output.html', 'w+').write(html_result)
    
#insert page title and copywrite year #this is all now in assemble_page using jinja
def page_title (page_name, output):
    page = open(output).read()
    if page_name == "index":
        title = "Home"
    else:
        title= page_name.capitalize()
    page_w_title = page.replace("{{title}}", title)
    #inserting current year
    now = datetime.datetime.now()
    year=str(now.year)
    page_w_date= page_w_title.replace("{{year}}", year)
    open(output, "w+").write(page_w_date)
        

#run--------------    
if __name__ == "__main__":
    main()
    
