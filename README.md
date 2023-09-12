# order_management
Order management

Background
Most of our API services are written in Python and Go:
● REST and GraphQL APIs written in Python/Django/Django REST Framework and Go
● Deployment on Debian/Debian derivative Linux servers, using Ansible for configuration
management. The day-to-day development is done on various flavours of *NIX; with a
range from MacOS to Arch Linux. A thorough knowledge of Linux is necessary for survival.
We are evolving slowly towards containerized deployment.
● PostgreSQL as the database of choice; although we don’t shy away from tangling with
Oracle or SQL Server when a client’s requirements demand so
The technical interview will be built around a coding assignment that is designed to screen for
the following basic skills:
● Experience in developing REST and GraphQL APIs in Python/Go/C#/Java
● experience with a configuration management tool e.g., Chef, Puppet, Ansible etc
● experience working with containers and container orchestration tools
● experience writing automated tests at all levels - unit, integration, and acceptance testing
● experience with CI/CD (any CI/CD platform)
We will be particularly interested in:

- Testing + coverage + CI/CD
- HTTP and APIs e.g., REST
- OAuth2
- Web security e.g., XSS
- Logic / flow of thought
- Setting up a database
- Version control

Screening Test
1. Create a simple Python or Go service
2. Design a simple customers and orders database (keep it simple)
3. Add a REST or GraphQL API to input / upload customers and orders:
- Customers have simple details e.g., name and code.
- Orders have simple details e.g., item, amount, and time.
4. Implement authentication and authorization via OpenID Connect
5. When an order is added, send the customer an SMS alerting them (you can use the
Africa’s Talking SMS gateway and sandbox)
6. Write unit tests (with coverage checking) and set up CI + automated CD. You can
deploy to any PAAS/FAAS/IAAS of your choice
7. Write a README for the project and host it on your GitHub
