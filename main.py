from website import create_app

app = create_app()

# If-statement used to make sure the website is run only when the file is run directly
if __name__ == "__main__":
    app.run(debug=True)