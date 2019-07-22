import os
import click

#register custom application commands
def register(app):

    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    #These functions are derived from the translate parent function
    #a standard way in which Click builds groups of commands
    @translate.command()
    #update function included both extract and update steps --
    #if successful, it will delete the messages.pot file after update
    #is complete
    def update():
        """Update all languages."""

        #if the command errors, raise a RunTimeError which causes the
        #the script to stop. 
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')


    @translate.command()
    #init command takes the new language code as an argument
    #click.argument defines the language code
    @click.argument('lang')
    #incorporate the argument lang into the init command
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    #these commands need to be enabled by importing them so that the
    #commands get registered
    #this gets put in the microblog.py file