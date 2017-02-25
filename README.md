# Facebook + Pyramid JWT minimal demo

This is a minimal tech demo showing how to exchange a Facebook user access
token (generated from a Facebook login) for a JWT token that can be used to
authenticate against Pyramid apps.

Getting Started
---------------

- Run ./install.sh

You need to have virtualenv installed on your system. If you don't have it,
look at the ``make_virtualenv.sh`` script in this folder, then adjust
install.sh

Register your Facebook app
---------------------------

You need to register for a new Facebook app, at https://developer.facebook.com
Enter your appid in the development.ini file.
