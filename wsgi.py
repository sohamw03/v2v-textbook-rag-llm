from yozu_pdf_pipeline.wsgi import application  # Replace with your Django app name


def main():
    """Function entry point"""
    gunicorn.run(
        "yozu_pdf_pipeline.wsgi:application",
        host="0.0.0.0",
        port=80,  # Use environment variable for port
        workers=3,  # Adjust worker count as needed
    )


if __name__ == "__main__":
    main()
