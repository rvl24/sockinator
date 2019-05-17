#The Idea

Pretty straightforward--use someone's foot measurements to make a custom knitting pattern.

#The Implementation
Flask was used to create a web application to serve this purpose. The app can be used to produce a pattern without creating
an account and logging in; registration is available for users who would like to save patterns.

Foot data (ick) are collected via a form, and the necessary stitch counts for each part of the sock are then computed in
Python. The results are handed over to a jinja2 template and stuck into a database table as a JSON blob if the user is logged in.

Logged-in users can access already-made patterns. All patterns created by the user are pulled from the database, and a page with a list of links to patterns is rendered. When a link is clicked, the pattern template is rendered with the stitch counts from the database. 
