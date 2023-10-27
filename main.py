from website import create_app

app=create_app()

# Entry point for the website
if __name__=='__main__': #ensures webserver runs only when this file is run
    app.run(debug=True) #debug true will rerun the code everytime a change is made,turn it false on prod

