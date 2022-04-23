#HCI Final Project -- DND Combat Management Tool

"Completed" features -- creating units (internally referred to as members), removing units, navigating between units, having units do actions, having units do actions to other units, and logging all actions done.

In other words, this is most of the non-specific functionality necessary to implement the whole project. Each action just needs their own related fields and action buttons, and units need more fields so that they can hold all necessary data (currently just hold name and id).

The current state of the project is extremely ugly as none of the styling or layout has been done (that is not my job, as the backend specialist). The functionality has, however, been written in such a way that it can easily be connected to much prettier html and css just by associating the right fields and buttons with the right ids.

To run this project, one must have flask and python3 installed. Set the environment variables `FLASK_APP=app.py` and `FLASK_ENV=development`. Then, simply navigate to the root of the project structure, and execute `flask run`. The app will then be reachable from localhost:5000.

Note that all data is stored in the browser session.
