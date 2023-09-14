# order_management
Order management

Background
Most of our API services are written in Python and Go:
-  REST and GraphQL APIs written in Python/Django/Django REST Framework and Go
-  Deployment on Debian/Debian derivative Linux servers, using Ansible for configuration
management. The day-to-day development is done on various flavours of *NIX; with a
range from MacOS to Arch Linux. A thorough knowledge of Linux is necessary for survival.
We are evolving slowly towards containerized deployment.
-  PostgreSQL as the database of choice; although we don’t shy away from tangling with
Oracle or SQL Server when a client’s requirements demand so


The technical interview will be built around a coding assignment that is designed to screen for
the following basic skills:
-  Experience in developing REST and GraphQL APIs in Python/Go/C#/Java
-  experience with a configuration management tool e.g., Chef, Puppet, Ansible etc
-  experience working with containers and container orchestration tools
-  experience writing automated tests at all levels - unit, integration, and acceptance testing
-  experience with CI/CD (any CI/CD platform)


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


# Order Management
This app helps manage orders for an e-comerce website.
The implimentation for this app is for a single tenant e-comerce platform
The applicaton has two front-end clients:
- The shopper's client
- The shopkeeper's client
This makes it easier to scale as a multitenant e-comerce application.

### The shopper's client
This is the shop front. 

It has the following features:
- As a shopper, I should see all the products
- As a shopper, I can select a specific product and see its details
- As a shopper, I should see how many items are remaining.
- As a shopper, I can place a single product in my cart
- As a shooper, I can add multiple units of the same product in my cart
- As a shopper, I can add multiple products in my cart
- As a shopper, I can remove items from my cart
- As a shopper, I can see all the price of all items in my cart
- As a shopper, I should get a notification when I place an order

### The Shopkeeper's client
This is the shopkeepers back office.

It has the following features.
- All the features in the shoppers client, this is for offline shoppers.
- As a shopkeeper, I should see all orders that have been made
- As a shopkeeper, I can accept or reject an order
- As a shopkeeper, I should see how many orders are pending fulfilment
- As a shopkeeper, I can add a product to the inventory
- As a shopkeeper, I can remove a product from the inventory
- As a shopkeeper, I can disable showing a product
- As a shopkeeper, I should be able to add employees
- As a shopkeeper, I should be able to give employees permisions

### Project Scope
**Phase One**: MVP (Shopkeeper's client)

The MVP will include the following:
-  **Products**; Adding, Reading, Editing, Deleting
-  **Orders**; Placing, Reading, Editing, Deleting, Rejecting, Fulfiling.
-  **Shoppers**; Registering, Login, Logout, Delete Acccount
-  **Shopkeeper**; Registering, Login, Logout, Delete Acccount

## Tech Stack

This section defines the technology used to develop the application.

 **Language**: Python

 **Framework**: Django

 **Testing**: Pytest
 
 **Protocol**: REST

 **Database**: PosgreSQL

 **Testing and Coverage** Travis CI & Coverage

 **Authentication & AUthorization**: OpenID Connect

 **Notification**: Africa's talking

## Testing criteria

**Live**: Link

**Setup**:


