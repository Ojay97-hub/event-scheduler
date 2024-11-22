## EVENTORY

**BRAND IMAGE**

![brand image](/static/images/validation/brand_image.png)

**"Connect People, Create Memories!"**

**REPSONSIVE SCREENSHOTS** 

![RESPONSIVE SCREENSHOTS](static/images/responsive_screenshots.png)

------ 

### INTRODUCTION
**WHAT THE PROJECT IS** 

EVENTORY is a dynamic web application designed to make event organisation and participation easy and efficient. Built with a user-centric approach, it serves as a comprehensive platform where event organisers can effortlessly create and manage events, while attendees can seamlessly browse, register, and participate in events that interest them. By fostering connections and creating lasting memories, EVENTORY aims to bridge the gap between organisers and attendees, enhancing the overall event management experience. 


**WHY IT EXISTS** 

In today’s fast-paced world, the event industry will benefit from a digitalised and accessible approach to organising and discovering events. EVENTORY addresses this need by providing a feature-rich platform that saves time, improves accessibility, and encourages meaningful engagement between organisers and attendees. Whether it’s a workshop, conference, or community gathering, EVENTORY is designed to make planning, managing, and attending events straightforward and enjoyable. This website was designed with care and due diligence to the user experience ensuring a smooth ride everytime. 


**WHO IS IT FOR** 

EVENTORY is great for the following three key user groups:

- Event Attendees: Individuals seeking to explore and participate in events that match their interests. The platform simplifies the process of discovering, registering for, and managing their attendance.
- Event Organisers: Professionals or enthusiasts who wish to create, manage, and oversee events effectively. EVENTORY provides organisers with tools to monitor registrations, communicate with attendees, and make updates in real-time.
- Platform Administrators: Moderators tasked with ensuring the quality and integrity of events listed on the platform. Admins have access to tools for managing all platform events, enforcing standards, and enhancing the overall user experience.

Whether you are hosting an event, attending one, or moderating the platform, EVENTORY is your go-to solution for connecting people and creating memories.

------
### Technologies
------
**Frontend**: HTML, CSS, Bootstrap, Javascript

**Backend**: Django, Python

**Database**: PostgreSQL

**Deployment**: Heroku

------
### WIREFRAMES 

#### LANDING PAGE
![LANDING PAGE]( /static/images/wireframes/home_page.png)
#### EVENT LIST
![EVENT LIST]( /static/images/wireframes/event_list_browsing.png)
#### EVENT DETAIL
![EVENT DETAIL]( /static/images/wireframes/event_detail.png)
#### CREATE & EDIT EVENT 
![CREATE AND EDIT PAGES](/static/images/wireframes/create_edit_events.png)
#### EVENT USER REGISTERED EVENTS
![EVENT USER EVENTS](/static/images/wireframes/users_registered_events.png)
#### ORGANISER CREATED EVENTS
![EVENT ORGANISER PAGE](/static/images/wireframes/organiser_created_events.png)
#### ORGANISER EVENT DETAIL
![EVENT ORGANISER PAGE](/static/images/wireframes/organiser_event_detail.png)
#### ATTENDEE LIST FOR ORGANISERS 
![ATTENDEE LIST](/static/images/wireframes/organiser_attendee_list.png)
#### SIGN UP PAGE
![SIGN UP](/static/images/wireframes/sign_up.png)

------
### CUSTOM MODELs
------

Below is the overview of all custom models used in this project including field name, field type, description, and relationships:

| **Model Name**   | **Field Name**      | **Description**                                                     | **Field Type**          | **Relationships**                                           |
|------------------|---------------------|---------------------------------------------------------------------|-------------------------|------------------------------------------------------------|
| **Location**     | venue_name          | Name of the venue                                                  | `CharField`             |                                                            |
| **Location**     | address_line_1      | Primary address of the location                                    | `CharField`             |                                                            |
| **Location**     | address_line_2      | Secondary address line (optional)                                  | `CharField`             |                                                            |
| **Location**     | town_city           | Town or city where the location is situated                        | `CharField`             |                                                            |
| **Location**     | county              | County or region of the location (optional)                         | `CharField`             |                                                            |
| **Location**     | postcode            | Postal code of the location                                        | `CharField`             |                                                            |
| **Location**     | is_online           | Boolean field to check if the event is online                       | `BooleanField`          |                                                            |
| **Event**        | title               | Title of the event                                                 | `CharField`             |                                                            |
| **Event**        | image_url           | URL to the event image                                             | `URLField`              |                                                            |
| **Event**        | start_date          | Date and time when the event starts                                | `DateTimeField`         |                                                            |
| **Event**        | end_date            | Date and time when the event ends                                  | `DateTimeField`         |                                                            |
| **Event**        | start_time          | Start time of the event                                            | `TimeField`             |                                                            |
| **Event**        | end_time            | End time of the event                                              | `TimeField`             |                                                            |
| **Event**        | location            | The location of the event                                          | `ForeignKey`            | ForeignKey to **Location** (A location can have many events) |
| **Event**        | organiser           | The user organizing the event                                      | `ForeignKey`            | ForeignKey to **User** (Each event has one organiser)      |
| **Event**        | description         | Description of the event                                           | `TextField`             |                                                            |
| **Event**        | capacity            | Maximum number of attendees                                        | `PositiveIntegerField`  |                                                            |
| **Event**        | category            | Category of the event (e.g., workshop, conference)                 | `CharField`             |                                                            |
| **Event**        | price               | Price of the event (optional)                                      | `DecimalField`          |                                                            |
| **Event**        | free                | Indicates whether the event is free                                | `BooleanField`          |                                                            |
| **Event**        | canceled            | Indicates if the event is canceled                                 | `BooleanField`          |                                                            |
| **Registration** | user                | The user who registered                                            | `ForeignKey`            | ForeignKey to **User** (A user can register for many events) |
| **Registration** | event               | The event the user registered for                                  | `ForeignKey`            | ForeignKey to **Event** (An event can have many registrations) |
| **Registration** | registered_at       | Timestamp when the user registered                                 | `DateTimeField`         |                                                            |

#### Relationships Summary:

Location has a one-to-many relationship with Event (One location can have many events).

Event has a many-to-one relationship with User (Each event is organized by one user).

Event has a many-to-one relationship with Location (Each event happens at one location).

Registration has a many-to-one relationship with both User and Event (Each registration is for one user and one event).

------
### AGILE METHODOLOGY 
------
This kanban based on the agile methodology approach is a visual representation of all the tasks, that comprised of main epic stories each with their own set of user stories. These were to be completed in order to finish the project successfully:
![KANBAN](/static/images/validation/kanban.png)

### Epic Stories and User Stories breakdown

### **Epic 1: Event Browsing and Discovery**
As an attendee, I want to easily browse, search, and discover events so that I can find the ones I’m most interested in and plan my participation.

| **Issue Number** | **User Story**                                                                 |
|------------------|---------------------------------------------------------------------------------|
| #1               | As an attendee, I want to view a list of upcoming events so that I can decide which event to attend. |
| #2               | As an attendee, I want to view the details of a specific event so that I can learn more about it. |
| #5               | As an attendee, I want to search for specific events by category or status so that I can speed up my search. |
| #7               | As an attendee, I want to see the event capacity and status so that I know if I can still register. |

### **Epic 2: Event Registration and Management for Attendees**
As an attendee, I want to manage my event registrations so that I can track my commitments and make changes as needed.

| **Issue Number** | **User Story**                                                                 |
|------------------|---------------------------------------------------------------------------------|
| #3               | As an attendee, I want to register for an event so that I can reserve a spot. |
| #4               | As an attendee, I want to view a list of events I have registered for so that I can track my commitments. |
| #6               | As an attendee, I want to cancel my registration if I can no longer attend so that I can release my spot. |

### **Epic 3: Event Creation and Management for Organisers**
As an organiser, I want to create, manage, and oversee my events so that I can engage attendees and ensure successful event execution.

| **Issue Number** | **User Story**                                                                 |
|------------------|---------------------------------------------------------------------------------|
| #8               | As an organiser, I want to create a new event so that people can register for it. |
| #9               | As an organiser, I want to view a list of all events I’ve created so that I can manage them efficiently. |
| #10              | As an organiser, I want to update the event details so that I can reflect any changes. |
| #11              | As an organiser, I want to delete an event that is no longer happening so that attendees can be notified. |
| #12              | As an organiser, I want to view a list of people who have registered for an event so I can see and contact who is attending. |

### **Epic 4: Event Search and Analysis for Organisers**
As an organiser, I want to search and analyse event data so that I can track trends, compare events, and improve my offerings.

| **Issue Number** | **User Story**                                                                 |
|------------------|---------------------------------------------------------------------------------|
| #14              | As an organiser, I want to search and filter events based on status, date, or category and organiser, so that I can analyse potential competitors. |

### **Epic 5: Platform Moderation for Admins**
As an admin, I want to oversee and moderate all events on the platform so that I can ensure high-quality and appropriate event entries.

| **Issue Number** | **User Story**                                                                 |
|------------------|---------------------------------------------------------------------------------|
| #15              | As an admin, I want to view a list of all events on the platform, so that I can moderate event entries to maintain platform quality. |
| #16              | As an admin, I want to filter or search through all events on the platform so that I can quickly access events that require attention. |


### MOSCOW Approach plan breakdown

## Event Attendees

| **User Story**                                                | **MoSCoW Priority** | **Category**   |
|---------------------------------------------------------------|---------------------|----------------|
| View a list of upcoming events (Event List)                   | Must-have           | Basic/Core     |
| View details of a specific event (Event Details)              | Must-have           | Basic/Core     |
| Register for an event (Event Registration)                    | Must-have           | Basic/Core     |
| View events I have registered for (View Registered Events)    | Should-have         | Good           |
| Search and filter events by category or status                | Should-have         | Good           |
| Cancel registration for an event                              | Should-have         | Good           |
| View event capacity and status                                | Could-have          | Extra          |

---

## Event Organisers

| **User Story**                                                | **MoSCoW Priority** | **Category**   |
|---------------------------------------------------------------|---------------------|----------------|
| Create a new event                                            | Must-have           | Basic/Core     |
| View a list of created events                                 | Must-have           | Basic/Core     |
| Edit event details                                            | Must-have           | Basic/Core     |
| Delete an event that is no longer happening                   | Should-have         | Good           |
| View a list of registered attendees                           | Should-have         | Good           |
| Manage event capacity                                         | Could-have          | Extra          |
| Search and filter created events                              | Could-have          | Extra          |

---

## Administrators

| **User Story**                                                | **MoSCoW Priority** | **Category**   |
|---------------------------------------------------------------|---------------------|----------------|
| View all events on the platform                               | Must-have           | Basic/Core     |
| Delete inappropriate or cancelled events (Event Moderation)   | Should-have         | Good           |
| Edit event details as an admin                                | Should-have         | Good           |
| Search and filter all platform events                         | Could-have          | Extra          |

------
### FEATURES

The features will be presented and explained in relation to the epic stories as these are the core objectives that outlined the project planning and structure.

------
#### **Epic 1**: Event Browsing and Discovery
------

##### #1: View a list of upcoming events:

- Displays a concise list of all upcoming events with key information such as the event name, date, and category.

- Serves as the first touchpoint for users to explore and discover events, making it easy to browse and decide which events to attend.

![EVENT LIST](static/images/features/event_list.png)

##### #2: View the details of a specific event:

- Provides detailed information about a selected event, including the description, date, time, location, capacity, and registration.

- Gives users the context and specifics they need to determine if they want to attend.

![EVENT DETAIL](static/images/features/event_detail.png)

##### #5: Filter specific events by category:

- Allows users to find an event based on categories such as music, tech, or fitness to ensure efficient event browsing.

- Helps users quickly find events relevant to their interests, enhancing usability and user satisfaction.

![CATEGORY FILTER](static/images/features/filter_by_category.png)

##### #7: See the event capacity:

- Displays the total capacity of an event and the number of remaining spots available. Shows how popular/unpopular the event is.

- Creates a sense of urgency and ensures users are aware of how many spots are left, encouraging timely registration. This aids event organisers events to reach maximum capacity in a timely manner.

![EVENT CAPACITY](static/images/features/event_capacity.png)

------
#### Epic 2: Event Registration and Management for Attendees
------
##### #3: Register for an event.

- Enables users to sign up for events they wish to attend.

- Fulfills the core purpose of the platform by connecting users with events and simplifying the registration process. Essential feature. 

![REGISTER TO EVENT](static/images/features/register_event.png)

![REGISTERED EVENT CARD](static/images/features/registered_card.png)

![REGISTERED EVENT CARD](static/images/features/registered_card.png)

![REGISTERED SUCCESS MESSAGE](static/images/features/success_registered.png)

##### #4: View a list of events I have registered for.

- Lists all events the user has successfully registered for.

- Provides users with an easy way to track their commitments and plan their schedule.

![REGISTERED EVENTS](static/images/features/my_registered_events.png)

##### #6: Cancel my registration if I can no longer attend.

-  Allows users to withdraw their registration from events.

- Empowers users to manage their attendance while freeing up spots for others, ensuring efficient event capacity management.

![CANCEL REGISTRATION](static/images/features/cancel_registration.png)

------
#### Epic 3: Event Creation and Management for Organisers
------
##### #8: Create a new event.

- Enables organisers to add events to the platform by specifying details like title, description, date, location, capacity, category, and price/free.

- Facilitates event creation, ensuring a steady flow of events for attendees to explore. Serves as a core feature of the project.

![CREATE EVENT](static/images/features/create_event.png)

##### #9: View a list of all events I’ve created.

- Displays all events an organiser has added to the platform.

- Centralises organisers events into one place so that they can manage their events effectively.

![CREATED EVENT](static/images/features/created_events.png)

##### #10: Update the event details.

-  Allows organisers to modify event information post-creation if any unseen changes or updates take place in the event preparations.

- Ensures event details remain accurate and up-to-date, improving reliability and trust for attendees.

![EDIT EVENT](static/images/features/edit_event.png)

![EDITING EVENT](static/images/features/editing_event.png)

![EDITED EVENT](static/images/features/edited_event.png)

![DISPLAY EDIT](static/images/features/displaying_edit.png)

##### #11: Delete an event that is no longer happening.

- Lets organisers remove events that are cancelled for unforeseen reasons or that they are no longer relevant.

- Helps maintain a clutter-free platform and avoids misleading attendees. Ensuring quality events are available for event browsers.

![DELETE EVENT](static/images/features/delete_event.png)

![DELETE SUCCESS](static/images/features/delete_success.png)

![DELETE DISPLAY](static/images/features/delete_display.png)

##### #12: View a list of people who have registered for an event to contact.

- Provides organisers with the contact details of registered attendees.

- Facilitates communication, enabling organisers to send updates or reminders about the event. This allows for transparent communication where necessary.

![ATTENDEE LIST](static/images/features/attendee_list.png)
------
#### Epic 4: Event Search and Analysis for Organisers
------
##### #14: filter events based on status, date, or category and organiser.

- Allows organisers to sort and filter their events by criteria such as other organisers, date range, or category etc.

- Helps organisers easily analyse and manage their events for better oversight and decision-making. Also allowing for organisers to see what competitors are doing on the platform for better competition and thus higher quality events for event users. 


![FILTER EVENTS](static/images/features/filter_events.png)

------
#### Epic 5: Platform Moderation for Admins
------
#####  #15: View a list of all events on the platform.

- Displays a complete list of events for administrative oversight. Editing and deleting functions are easy to implement. 

- Enables platform admins to monitor the content and ensure compliance with guidelines.

![ADMIN EVENT VIEW](static/images/features/admin_view.png)

#####  #16: Filter through all events on the platform.

- Lets admins sort and filter events based on various criteria such as category, date, or price/free.

- Simplifies moderation tasks, allowing admins to manage platform events efficiently and maintain quality, by pinpointing the appropriate events with ease.

![ADMIN FILTER](static/images/features/admin_filter.png)

------
#### User authentication 
------

EVENTORY implements a robust authentication system to ensure secure access and personalised user experiences:

**User Roles and Access**

Event Attendees: Can browse events, register, and manage their registrations.
Event Organisers: Additional permissions to create, edit, and manage events but cannot register for events.
Admins: Elevated access to moderate all events and manage platform content

**Sign-Up**

- New users can create an account by providing:
- Username
- Email address
- Password (confirmed with a repeat entry for validation).
- Choose user type; event user or event organiser using django groups.

**Role-Based Features**

Navigation and dashboard options dynamically adjust based on the user’s role:

- Organisers see "My Events", "Create Event", and "Events" 
 
- Attendees see only "My Events" and "Events" 

**Authenticated and Unauthenticated users**

Logged in users - attendee vs organiser (authenticated).

Not logged in users (unauthenticated).

**Authenticated**

- Event users will see register for event.
- Event users will see status reports i.e.: 
    - you are already registered for this event
    - This event has already taken place sign up to the next one.

- Event organisers will see edit, cancel and view attendee list (if they are the organiser).
- Event organisers will see, "login as an event user to register for this event!" if not owners of the event. 

**Unauthenticated**

- These users will see, "Please log in to register for this event". 

In summary, there are clear user roles and different authentication based on what user type.  

------
### TESTING
------
#### LIGHT HOUSE

Importantly the accessibility, best practices, and SEO have all scored 100/100. 

Performance has been fairly impacted due to:

- Use video formats for animated content Potential savings of 594 KiB

- Largest Contentful Paint element 7,420 ms

- Eliminate render-blocking resources Potential savings of 1,380 ms

- Remove duplicate modules in JavaScript bundles Potential savings of 13 KiB

- Reduce unused CSS Potential savings of 35 KiB


HOME PAGE

![ACCESSIBILITY 100](static/images/testing/accessibility_100.png)

EVENT LIST

![EVENT LIST LIGHTHOUSE](static/images/testing/eventlist_lighthouse.png)

EVENT DETAIL

![EVENT DETAIL LIGHTHOUSE](static/images/testing/eventdetail_lighthouse.png)
------
#### RESPONSIVENESS
------

Using bootstrap comes with a lot of predetermined website responsiveness on all devices. I also implemented some custom responsiveness using media queries - this has resulted in all templates being responsive.  

| **File Name**       | **Responsiveness**   |
|---------------------|----------------------|
| `Sign up`           | PASS                 |
| `Home`              | PASS                 |
| `Event list`        | PASS                 |
| `Event detail`      | PASS                 |
| `Create event`      | PASS                 |
| `Edit`              | PASS                 |
| `Registered events` | PASS                 |
| `Created events`    | PASS                 |
| `Attendee list`     | PASS                 |


------
#### Validation
------
This validation was processed by using Heroku's URL into the URI validator with W3C. Other key validators included:
- W3C CSS
- JSHint 
- Code Institute Python Linter for PEP8 compliance

Validation table for HTML templates:

| File Name           | Purpose                                                                 | W3C Validation Status              |
|---------------------|-------------------------------------------------------------------------|-------------------------------------|
| `Sign up`          | The sign-up page where users can register for an account.                | PASS                              |
| `Home`             | The homepage displaying an overview and key actions for the application. | PASS                             |
| `Event list`       | Lists all available events for users to browse and register.             | PASS                           |
| `Event detail`     | Displays detailed information about a specific event.                   | PASS                              |
| `Create event`     | Allows event organisers to create a new event.                          | PASS                             |
| `Edit`             | Enables event organisers to edit an existing event.                    | PASS                              |
| `Registered events`| Shows the list of events a user has registered for.                     | PASS                              |
| `Created events`   | Displays the list of events created by an organiser.                    | PASS                              |
| `Attendee list`    | Provides a list of attendees for a specific event (visible to organisers). | PASS                              |

#### Screenshots of Validation

**TEMPLATES** 

Sign Up

![SIGN UP](/static/images/validation/sign-up_pass.png)

Home Page

![HOME](/static/images/validation/home_pass.png)

Event List

![EVENT LIST](/static/images/validation/event_list_pass.png)

Event Detail

![EVENT DETAIL](/static/images/validation/event_detail_pass.png)

Create Event

![CREATE EVENT](/static/images/validation/create_event_pass.png)

Edit Event

![EDIT EVENT](/static/images/validation/edit_event_pass.png)

Registered Events

![REGISTERED EVENTS](/static/images/validation/my_events_pass.png)

Created Events

![CREATED EVENTS](/static/images/validation/my_events_pass.png)

Attendee List

![ATTENDEE LIST](/static/images/validation/attendee_list_pass.png)


Validation table for CSS, Javascript and Python:
| File Type   | File Name               | Purpose                                                                 | Validation Status                  |
|-------------|-------------------------|-------------------------------------------------------------------------|------------------------------------|
| CSS         | `style.css`            | Contains styles for the overall look and feel of the application.       | Valid (Checked with W3C CSS Validator) |
| JavaScript  | `script.js`            | Handles interactivity and event-driven functionality on the frontend.    | Valid (Linted with ESLint)         |
| Python      | `settings.py`          | Contains configuration settings for the Django project.                 | Valid (PEP8 Compliant)             |
| Python      | `views.py`             | Defines the logic and rendering for various web pages.                  | Valid (PEP8 Compliant)             |
| Python      | `models.py`            | Defines the data models for the application.                            | Valid (PEP8 Compliant)             |
| Python      | `forms.py`             | Contains form definitions for user input validation and handling.        | Valid (PEP8 Compliant)             |
| Python      | `urls.py`              | Maps URL paths to views for the Django application.                     | Valid (PEP8 Compliant)             |
| Python      | `admin.py`             | Registers models in the Django admin interface.                         | Valid (PEP8 Compliant)             |
| Python      | `signals.py`           | Contains signal handlers for event cancellations    | Valid (PEP8 Compliant)             |
| Python      | `context_processors.py`| Adds custom data for event user & organisers groups             | Valid (PEP8 Compliant)             |

#### Screenshots of Validation

**CSS**

![CSS](/static/images/validation/css_pass.png)

**JAVASCRIPT**

![CSS](/static/images/validation/javascript_pass.png)

**PYTHON**

Settings

![SETTINGS](/static/images/validation/settings_pass.png)

Views

![VIEWS](/static/images/validation/views_pass.png)

Models

![MODELS](/static/images/validation/model_pass.png)

Forms

![FORMS](/static/images/validation/forms_pass.png)

Urls

![URLS](/static/images/validation/urls_pass.png)

Admin

![ADMIN](/static/images/validation/admin_pass.png)

Signals

![SIGNALS](/static/images/validation/signals_pass.png)

Context Processors 

![CONTEXT PROCESSORS](/static/images/validation/context_processor_pass.png)



### MANUAL TESTING

In this section I showcase the key feature tests from a user perspective through manual testing ensuring a smooth experience throughout.

#### FORMS

There are two key forms in this website - the signup, registering for an event and the create/edit events forms. 

**SIGN UP FORM VALIDATION**


![SIGN UP USERNAME](static/images/testing/username_valid.png)

![SIGN UP EMAIL](static/images/testing/email_valid.png)

![SIGN UP EMAIL 2](static/images/testing/email_valid2.png)

![SIGN UP PASSWORD](static/images/testing/signup_password.png)

![SIGN UP PASSWORD 2](static/images/testing/signup_password2.png)

![SIGN UP NO MATCH PASSWORD](static/images/testing/nomatch_password.png)

![SIGN UP SUCCESS](static/images/testing/signup_success.png)

**CREATE EVENT FORM** 

![CREATE TITLE](static/images/testing/enter_title.png)

![CREATE ENDDATE](static/images/testing/enter_enddate.png)

![CREATE STARTTIME](static/images/testing/enter_starttime.png)

![CREATE ENDTIME](static/images/testing/enter_endtime.png)

![CREATE IMAGE](static/images/testing/enter_image.png)

![CREATE IMAGE URL](static/images/testing/enter_imageurl.png)

![CREATE DESCRIPTION](static/images/testing/enter_description.png)

![CREATE CAPACITY](static/images/testing/enter_capacity.png)

![CREATE PRICE](static/images/testing/enter_priceifpay.png)

![CREATE VENUE](static/images/testing/enter_venue.png)

![CREATE ADDRESS1](static/images/testing/enter_address1.png)

![CREATE TOWN](static/images/testing/enter_town.png)

![CREATE POSTCODE](static/images/testing/enter_postcode.png)

![CREATE REDIRECT](static/images/testing/createdevent_redirect.png)

**EDIT EVENT FORM**

![EDIT EVENT](static/images/testing/editevent_success.png)

**EVENT CAPACITY FULL**

![EVENTLIST CARD FULL](static/images/testing/full_eventcard.png)

![EVENTDETAIL CARD FULL](static/images/testing/eventdetail_full.png)

**REGISTER FOR AN EVENT**

![EVENT REGISTER ENTER EMAIL](static/images/testing/register_addemail.png)


![EVENT REGISTER SUCCESS](static/images/testing/registration_success.png)

![EVENT DETAIL CONFIRM](static/images/testing/eventdetail_confirmreg.png)

![EVENT REGISTERED EVENTS](static/images/testing/registered_events.png)

**EVENT LIST FILTER**

Online filter showing online events.

![FILTER ONLINE PASS](static/images/testing/filter_online.png)

In-person events filter working.
![FILTER INPERSON PASS](static/images/testing/filter_inperson.png)

Free events filter working.
![FILTER FREE EVENTS PASS](static/images/testing/filter_freeevents.png)

Filtering by organiser also working.
![FILTER BY ORGANISER](static/images/testing/filter_byorganiser.png)
------
#### Button Test Table
------

**BASE TEMPLATE**

| **Button**                  | **Location in File**      | **URL/Function**                                    | **Functional** |
|-----------------------------|---------------------------|----------------------------------------------------|----------------|
| **Home**                    | Navbar                   | `'home'`                                 | Pass           |
| **Events**                  | Navbar                   | `event_list`                           | Pass           |
| **Create Event**            | Navbar (for organisers)  | `create_event`                         | Pass           |
| **My Events** (Organiser)   | Navbar (for organisers)  | `created_events`                       | Pass           |
| **My Events** (User)        | Navbar (for users)       | `registered_events`                    | Pass           |
| **Logout**                  | Navbar                   | `account_logout`                       | Pass           |
| **Register**                | Navbar (if not logged in)| `account_signup`                       | Pass           |
| **Login**                   | Navbar (if not logged in)| `account_login`                        | Pass           |
| **Facebook Icon**           | Footer                  | `<a href="https://www.facebook.com" target="_blank">` | Pass           |
| **Twitter Icon**            | Footer                  | `<a href="https://www.twitter.com" target="_blank">` | Pass           |
| **Instagram Icon**          | Footer                  | `<a href="https://www.instagram.com" target="_blank">` | Pass           |
| **YouTube Icon**            | Footer                  | `<a href="https://www.youtube.com" target="_blank">` | Pass           |


**HOME PAGE**

| **Button**                        | **Location in File**         | **URL/Function**                                    | **Functional** |
|-----------------------------------|------------------------------|----------------------------------------------------|----------------|
| **Create Event**                  | Hero Section (if organiser)  | `create_event`                         | Pass           |
| **Browse Events**                 | Hero Section (if user)       | `event_list`                           | Pass           |
| **Sign Up**                       | Hero Section (if not logged in) | `account_signup`                    | Pass           |
| **Log In**                        | Hero Section (if not logged in) | `account_login`                     | Pass           |
| **Previous Slide**                | Hero Image Carousel          | Carousel button to move to the previous slide     | Pass           |
| **Next Slide**                    | Hero Image Carousel          | Carousel button to move to the next slide         | Pass           |
| **View Events**                   | Call to Action Section       | `event_list`                           | Pass           |


**ATTENDEE LIST**

| **Button**                  | **Location in File**      | **URL/Function**                                    | **Functional** |
|-----------------------------|---------------------------|----------------------------------------------------|----------------|
| **Contact**                 | Table (Attendee list)    | `mailto: registration.user.email`             | Pass           |
| **Back to Event Details**   | Below Attendee List      | `event_detail event.id`                | Pass           |


**CREATE EVENT PAGE**

| **Button**               | **Location in File**       | **URL/Function**                                   | **Functional** |
|--------------------------|----------------------------|---------------------------------------------------|----------------|
| **Create Event**         | Bottom of the form         | Submits the form to create a new event            | Pass           |

**UPDATE EVENT PAGE**

| **Button**               | **Location in File**       | **URL/Function**                                   | **Functional** |
|--------------------------|----------------------------|---------------------------------------------------|----------------|
| **Update Event**         | Bottom of the form         | Submits the form to update the event details      | Pass           |


**CREATED EVENTS PAGE**

| **Button**               | **Location in File**         | **URL/Function**                                   | **Functional** |
|--------------------------|------------------------------|---------------------------------------------------|----------------|
| **Create New Event**      | Above the events list        | `create_event`                         | Pass           |
| **Manage**                | In each event card footer    | `event_detail event.id`               | Pass           |
| **Create One Now**        | If no events exist           | `create_event`                         | Pass           |


**EVENT DETAIL PAGE**

| **Button**                        | **Location in File**                 | **URL/Function**                                    | **Functional** |
|-----------------------------------|--------------------------------------|----------------------------------------------------|----------------|
| **Edit Event**                    | Inside "Manage Buttons" section      | `{% url 'edit_event' event.id %}`                  | Pass           |
| **Cancel Event**                  | Inside "Manage Buttons" section      | Opens the modal to cancel the event               | Pass           |
| **View Attendee List**            | Inside "Manage Buttons" section      | `attendee_list' event.id`               | Pass           |
| **Register**                      | Registration form for event users    | Submits the form to `event_register' event.id` | Pass           |
| **Back to Events List**           | Navigation buttons below the card    | `event_list`                           | Pass           |
| **Back to My Events** (Organiser) | Navigation buttons below the card    | `created_events`                       | Pass           |
| **Back to My Events** (User)      | Navigation buttons below the card    | `registered_events`                    | Pass           |
| **Close**                         | Cancel Event Modal                   | Closes the modal                                   | Pass           |
| **Yes, Cancel Event**             | Cancel Event Modal                   | Submits the form to `delete_event event.id` | Pass           |



**EVENT LIST PAGE**

| **Button**                        | **Location in File**           | **URL/Function**                                    | **Functional** |
|-----------------------------------|--------------------------------|----------------------------------------------------|----------------|
| **Toggle Filters**                | Filter Section                 | Toggles visibility of the filter panel             | Pass           |
| **Filter**                        | Inside Filter Panel            | Submits the filter form                            | Pass           |
| **More Info**                     | Event Cards (for organisers)   | `event_detail event.id`                | Pass           |
| **View Event**                    | Event Cards (for users)        | `event_detail event.id`                | Pass           |
| **Register**                      | Event Cards (for users)        | `event_register event.id`              | Pass           |
| **Registered**                    | Event Cards (for registered users) | Disabled button indicating the user is registered | Pass           |
| **Previous Page**                 | Pagination Section             | Navigates to the previous page in pagination       | Pass           |
| **Page Numbers**                  | Pagination Section             | Navigates to a specific page in pagination         | Pass           |
| **Next Page**                     | Pagination Section             | Navigates to the next page in pagination           | Pass           |

**REGISTERED EVENTS PAGE**

| **Button**               | **Location in File**            | **URL/Function**                                    | **Functional** |
|--------------------------|---------------------------------|----------------------------------------------------|----------------|
| **View Event**           | Upcoming Events section         | `'event_detail' registration.event.id `    | Pass           |
| **Cancel Registration**  | Upcoming Events section         | Submits form to `'unregister_from_event' registration.event.id` | Pass |
| **View Event**           | Today's Events section          | `event_detail' registration.event.id`    | Pass           |
| **Cancel Registration**  | Today's Events section          | Submits form to `'unregister_from_event' registration.event.id` | Pass |
| **View Event**           | Past Events section             | `'event_detail' registration.event.id`    | Pass           |


------
#### Bugs 
------
##### Unresolved bug
Comment section for under the event detail card: 
- Being a django based project the javascript for the comment section didn't respond well with the html and caused syntax errors. I then focussed on separation of concerns, adding the javascript into its own dedicated file, but without the onclick inline attributes within the html document it didn't go as expected. I then decided to leave the comment section out of the project given it is a 'could have' feature, in regards to the MOSCOWm, and would strongly consider it as a future feauture. 

------
### DEPLOYMENT
------

#### Github pages (local)


#### Heroku (production)

------
### FUTURE FEATURES
------
#17 As an **event attendee** I would like to **write comments under the event detail** to **discuss with other attendees and leave positive reviews**

------

#18 As an **event organiser** I want to **write a bio on my page** so that **suitable organisers can connect with me**

------
### CREDITS
------

- Balsamiq for the wireframes
- Bootstrap layouts
- Favicon.io for custom favicon
- Font Awesome for icons
- Google Fonts for custom fonts
- Django for the backend framework
- Code Institute Python Linter
- unsplash for stock images




