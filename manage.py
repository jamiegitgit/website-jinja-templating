import utils
import sys



#run--------------    
if __name__ == "__main__":   
    print("This is argv:", sys.argv)
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "build":
            print("Build was specified")
            utils.build()
            print("Your content pages are now templated into your website design")
        elif command == "new":
            print("New page was specified")
            utils.new()
            print("A new content page has been created at content/new.html")
        else:
            print("Usage:")
            print("  To rebuild site: python manage.py build")
            print("  To create new page: python manage.py new")
    else:
        print("Usage:")
        print("  To rebuild site: python manage.py build")
        print("  To create new page: python manage.py new") #DRY... :/

    
    

