# Docrates

Welcome to Docrates, a centralized app that stores all your medical information in one place and makes it accessible through a simple interface.

## Prod Environment

The prod environment is currently being set up. We are working on setting up the prod environment and making it accessible to the public. Please be patient as we are working on this.

[Click here to access the prod environment](https://docrates.de/)

## Development Environment

The development environment is currently being set up. We are working on setting up the development environment and making it accessible to the public. Please be patient as we are working on this.

- [Click here to access the development environment](https://dev.docrates.de/)
- [Click here to access the development environment (Neo4j)](http://itbt.org:7474/browser/)
- [Click here to access the development environment (MongoDB)](http://itbt.org:27017/)
- [Click here to access the development environment (Gitlab)](http://gitlab.itbt.org/docportal/docportal)

## Name Change

The project was originally called "Docportal" but was changed to "Docrates" due to a name conflict with another project. The name "Docrates" is a combination of the words "Doctor" and "Socrates".
The "Doctor" part of the name represents the medical aspect of the project and the fact that it is a medical information portal, while the "Socrates" part of the name represents the knowledge that the project provides for the user about their medical information.

## Stage of Development

The current stage of development is beyond a working MVP. We are actively working on connecting the frontend to the backend and expanding functionality as we progress. Please note that this readme and the documentation are still in progress.

The backend is well-documented and accessible via a [web interface](http://itbt.org:7474/browser/). The last time I checked, it didn't ask for a password, but I'm pretty sure it has one and autologged me.

### Branches

- `main`: The main branch is the default branch and is protected. Do not push into this branch!
- ~~`mvp`: The MVP branch is the branch that contains the MVP (Minimal Viable Product). It is protected. Do not push into this branch!~~
- `dev`: The dev branch is the development branch. This is where all the development happens. Please push into this branch if you are working on a feature or a bug fix.
- `feature/*`: The feature branches are branches that are created for a specific feature. Please create a feature branch if you are working on a feature.
- `bugfix/*`: The bugfix branches are branches that are created for a specific bug fix. Please create a bugfix branch if you are working on a bug fix.
- `hotfix/*`: The hotfix branches are branches that are created for a specific hotfix. Please create a hotfix branch if you are working on a hotfix.
- `release/*`: The release branches are branches that are created for a specific release. Please create a release branch if you are working on a release.

### Special Rules

You are allowed to push into the `main` branch if you:

- Are fixing a critical bug
- Are fixing a security issue
- Are documenting the code you forgor to document
- Are updating the README.md file or the documentation
- Are updating the license
- Are updating the `.gitignore` file
- Are updating the `.gitlab-ci.yml` file

> please for the love of god don't push into main if you are not doing any of the above

### Sidenote

If you push to main and it's not a quick fix or something small but rather some breaking changes, you will have the honorable task to stay up all night and fix all the merge conflicts you created :) ... and you die ... but after you fix your code ... but you will die. 

So, remember to tread carefully with those main pushes!

Happy coding! And remember, the flames of hell and the gulag next door are looking for you if you write bad code and waste resources!


## MVP

The MVP (Minimal Viable Product) ~~can be found in the 'mvp' branch and is protected. Do not push into this branch!~~

**Note:** Although we have ensured that the database connection is no longer active, providing it with a real Neo4j connection makes it fully usable. Please make sure you don't use the production URL, as it will work and it will break things! So, please, just don't.

If you do: BE WARNED! We know who you are, we have a backup, but you WILL be dead. THERE WILL BE NO WITNESSES!

> Unfortunately the MVP is no longer available. If you for some reason need access to the MVP, please contact Leon Prinz, he has a backup of the MVP on a Hard Drive.

## Note for All Devs

If you don't use Flask macros for anything more than a simple string: consider the gulag next door because that's where you're staying if another one of you wastes another 2 days because we need to make a macro out of your HTML that you pasted in from ChatGPT!

## Archive 

The Archive contains old information that was in the README.md file. This information is now outdated and is only kept for archival purposes.

If you want to access the archive, you can do so by clicking [here](archive.md).

## Performance

### New Architecture (itbt 1)

- 16 Core/32 Thread Xeon
- 64GB RAM
- 2TB SSD Storage
- 10TB HDD Storage
- 1000mbps Glass Fiber from Deutsche Glasfaser
- finally a DMZ that is not a Mac Mini
- nginx reverse proxy (that is currently dying a bit)
- neo4j database and mongoDB (both running on docker)
- a gitlab runner that is actually working
- a prod environment is a big to-do
- backups are a big to-do as well
- a working internet connection (no more incidents so far) (knock on wood)

> This is the new architecture that we are currently using. It is smaller computer-wise, but it is more efficient and has more storage. We are currently working on setting up the prod environment and the backups.

> If you somehow manage to overload the new Server, then we will send you a happy letter containing an invitation to a public beating + the electricity bill.

> The Old Architecture was a bit overkill on quantity, everything was unorganized, but we had to use it because we had no other server. Now we have a server that is actually meant for this kind of stuff, so please don't overload it.

## Special Thanks

Special thanks and a Farewell to Arthur Ladner for your help with the backend and the database. We will miss you and your help! Hopefully, you will be able to help us in the future as well!

## License

This project is licensed under an "internal source license". Please contact the project owners for more information as this is a private project.
As this is a WIP project, the license is not yet defined.
But in the meantime, please don't steal our code if youre not a part of the project. We worked hard on it and we don't want it to be stolen.
If you are a part of the project: Diggah ich glaub jeder von uns hat schonmal was von der Codebase geklaut... aber wehe du verbesserst den Code irgendwo anders und bringst es nicht hierher! Dann gibt's auf die Fresse!

## Contributors

- Arthur Ladner
- Eric Weisbrod
- Leon Prinz
- Christopher Schreck
- Davide Castiglione
- Yannik Müller

## Contact

If you have any questions or concerns, please contact the project owners or the contributors. We are happy to help you with any questions you may have.
Email: info@docrates.de

## Acknowledgements

- [Neo4j](https://neo4j.com/)
- [MongoDB](https://www.mongodb.com/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Docker](https://www.docker.com/)
- [Gitlab](https://about.gitlab.com/)
- [Nginx](https://www.nginx.com/)
- [Deutsche Glasfaser](https://www.deutsche-glasfaser.de/)
# pythontest
