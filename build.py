# todo:
#-get rid of search bar
#- get rid of made with heart
#- make photos smaller
#- change input and output files to be diff


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
    #create_menu(list_of_pages)
    create_interior_files()
    #create_full_base()
    #assemble each page 
    for page in list_of_pages:
        title= page["title"]
        interior= page["stage"]
        output= page["output"]
        #add in filename and output so can use them
        #base= assign_base(title)
        assemble_page(title, interior, output)           

# begin with base, headerfooter, content files
#create fullbase
#put menu in fullbase and content/index
#put title, content, and date in base and fullbase

#what if i begin with fullbase and use jinja to comment out header and footer?
    #can't comment out header and footer
#then i can assemble title, content, date in base
#then insert menu
#can i do all rendering at once? adding in {{begin_comment}} and {{end_comment}}
#will still have to render menu within the index content page       
#either two render codeblocks or looped rendering where it repeats unnecessarily     

#build the list of pages automatically
def create_list_of_pages():
    all_html_files = glob.glob("content/*.html")
    for page in all_html_files:
        print(page) #delete later
        #file_path = page
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

#step 2
#put content in header template, but just copy index over
def create_interior_files():
    for page in list_of_pages:
        print(page["title"], page["input"], page["stage"]) #delete
        # copy index.html from contents to interior
        page_content=open(page["input"]).read()
        if page["title"] == "Home":
            interior_file=page_content
        else:
            header_footer=open("templates/headerfooter.html").read()
            template = Template(header_footer)
            interior_file = template.render(
                content=page_content,
            )
        open(page["stage"], "w+").write(interior_file)




#generate a menu from the list_of_pages 
def create_menu(pages):
    header_footer = open("templates/headerfooter.html").read()
    #generate menu link for each page
    for page in pages:
        title = page["title"]
        if title == "Home":
            template_file= open("content/index.html").read() #i can't make input and output file be same
            output_file = "content/indexwmenu.html"
        else:
            template_file = header_footer
            output_file = "templates/headerfooterwmenu.html"
        #place menu in  template
        template = Template(template_file) 
        menu_inserted = template.render( #this actually renders templates/headerfooter.html twice. is that good? bad?
            pages= pages,
        ) 
        open(output_file, "w+").write(menu_inserted)
    

# Create full base with header and footer    
def create_full_base():
    #open basic base
    base_template = open("templates/base.html").read()
    # Read in the header and footer
    header_footer = open("templates/headerfooter.html").read()
    # Add header and footer to basic base
    template = Template(base_template)
    full_base=template.render(
        header_footer=header_footer,
        title ="{{title| title}}", #this pass destroys the title, so have to re-insert it
    )  
    open("templates/fullbase.html", "w+").write(full_base)     
       
# Chooses correct base for each page
def assign_base(page_name):
    base = None
    #index gets basic base, others get full base    
    if page_name == "Home":
        base = open("templates/base.html").read()
    else:
        base = open("templates/fullbase.html").read()
    return base
       
            
#replace placeholder in each page with the page's content, title, year
def assemble_page(page_name, interior_file, output):
    # Define inside, title, and year (add menu)
    inside = open(interior_file).read()
    base= open("templates/base.html").read()
    now = datetime.datetime.now()
    year=str(now.year)
    print(page_name, interior_file, output)
    #template to put it all together
    template = Template(base)
    finished_page=template.render(
        content = inside,
        title = page_name,
        year = year,
        #menu,
    )  
    open(output, "w+").write(finished_page)    

        

#run--------------    
if __name__ == "__main__":
    main()
    
