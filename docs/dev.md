# Developer Documentation

If you want to hack on CTFlex or understand how it works, you’ve come to to the right place! If you are just looking to host your own CTF, you can check out the [host documentation](./host.md). Make sure you’ve read the host documentation before this document.

## Overview of Design

### Why the design is not MVC

MVCs are appropriate for updating state in a graphical program: User → Controller → Model → View → User. With requests, there simply isn’t much state as they are practically instantaneous.

Yes, there are sessions, but, really, they’re just for authentication and flashing. The only time there is state is with client-side live updating with sockets like the stretch goal of a live scoreboard and, somewhat, submitting flags using AJAX instead of page refreshes. Then, we might use a JS library like Kendo for the client-side state.

### Django’s MVT Design

Django uses what might be acronymized as ‘MVT.’ Views are like the controllers. They receive requests, talk to the Model (more on this later), and then send off that data to Templates. Templates are like views, but very dumb ones at that. Models are Django’s ORM around the database.

Now, how do Views talk to the model? For simple queries, they do so directly. What about complex interactions? Django makes it super easy for models to include lots of ‘business logic.’ However, this framework shall resist this temptation and keep models as thin wrappers. Complex interactions will go through the bags of functions ‘Commands’ and ‘Queries.’

### Queries and Commands

Models should contain logic related only the the schema. Templates will necessarily depend on the models. However, views either go through queries or are simple enough that a class like DetailView would be more appropriate for it.

A query is recommended when:

- it is read based on not just schema but app logic (e.g., eligibility)
- it is a cross-model read

All writes should go through commands. Commands are especially needed when:

- it is performing non-database operations like sending emails
- it is a cross-model write

Because of this choice, we can see exactly which kind of queries we are making and perhaps restructure, denormalize, or cache as appropriate.

We will also be able to test easily.

This design is heavily influenced by a functional paradigm of programming as opposed to the typically more object-oriented style of software design.

## Where’s what?

This diagram traces the flow of data through the framework:

![Data Flow diagram](./Data Flow.png)

When a request for a non-static file arrives, Django looks in `urls.py` to route the URL to a view. Then, the view is called with any arguments captured from the URL. This view then uses queries and commands to get information from the models or or manipulate them.

Queries and commands are explained [above](#queries-and-commands). Both of them deal with models or emails or loading problems etc. Models are just very simply classes which tell Django what tables and fields to create. Models also provide validation.

Once the view has talked to queries and commands, it collects information up into a variable called `context` and renders a template in the context of `context`. A template is an HTML file that is preprocessed using Django Template Language and can change dynamically based on `context`.


## Development Lifecycle 

### Updating remote servers without losing data

1. Pull from your origin repo using `git pull`
1. Install any new Python packages using `pip install -r requirements.txt`
1. Restart the app server (if you are using Supervisor, use `sudo supervisorctl restart pactf`)
1. If you are using nginx, validate and update nginx configuration using `sudo nginx -t && sudo service nginx restart`

### Flushing the database and starting over

Run `manage.py reloaddata`. If it fails, you can try running `manage.py reset_db`. If _that_ fails, use `initializedb.sql`.

### Contributing changes

In your [fork](https://help.github.com/articles/fork-a-repo/) of this repository, create a branch with your changes and submit a [pull request](https://help.github.com/articles/using-pull-requests/). You may contact us at the emails specific in the [README](../README.md).


## Style Guidelines

### Docstrings

Write a docstring for any function or class whose implementation is longer than a few lines and whose purpose is not blindingly obvious.
Write a docstring for all Python files except for files defining Django management commands, which much be documented in the help attribute of the commands’ respective classes.

Format docstrings as sp:

    """Compute the side length of a square given its area
    
    Purpose:
        <Explanation of why the documented thing exists>
        
    Usage:
        <Full description of interface of the documented thing (or whether it is automatically called etc.)>
        
    Implementation Notes:
        - <Particular choices made as relevant to the interface>
        - ...
    """
    
### Imports

Imports for Python files fall into one of the following categories:

- Standard Library modules
- Django modules included with Django (or part of the `contribs` package)
- 3rd-party non-Django modules
- 3rd-party Django modules
- 1st-party/your/intra-package modules

Group imports of the same category. Separate such groups with a blank line. Order the groups in the order above.


## What else?

### State of the Documentation

The templates and `settings.py` are relatively undocumented; everything else should be documented (if not, create an issue!).


### Where do I start?

Start by looking at:
 
- `models.py`
- `queries.py` and `commands.py`
- `views.py`
- `urls.py`
- `base.template.html`

This should conclude your basic tour of the lifecycle of a request. You might then want to look at:

- `ctflex/constants.py`
- `ctflex/settings.py`
- `settings.py`

The rest of the files you can look at as needed/come across.
