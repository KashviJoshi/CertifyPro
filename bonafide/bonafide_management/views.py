from django.shortcuts import render, redirect
from .models import Student, CustomUser
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import  StudentForm, CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse
from django.http import JsonResponse, HttpResponseForbidden
# from bonafide_management.models import Customer
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random 
from django.conf import settings
from django.core.mail import send_mail


@login_required(login_url='/login/')  # Ensure the user is logged in to access this view
def bonafide_details(request):
    # Your view logic goes here
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bonafide_details')  # Redirect to the same page after successful form submission
    else:
        form = StudentForm()

    return render(request, 'bonafide_details.html', {'form': form})

def student_registration(request):
    # Add any logic you need for student registration
    return render(request, 'student_registration.html')

def admin_login(request):
    return render(request, 'admin_login.html')

# def bonafide_details(request):
#     students = Student.objects.all()
#     # Your view logic goes here
#     return render(request, 'bonafide_details', {'students': students})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if the email domain is allowed
            if email.endswith('@birlainstitute.co.in'):
                # Generate OTP
                otp = generate_otp()

                # Save the OTP in the session for verification
                request.session['signup_otp'] = otp

                # Send OTP to user's email
                send_otp_email(email, otp)

                # Redirect to OTP verification page
                return render(request, 'otp_verification.html')

            else:
                messages.error(request, "Email domain not allowed.")
        else:
            messages.error(request, "Invalid form submission. Please check the form fields.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'student_registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        error = "Invalid Credentials"

        # Check if the email domain is allowed
        if email.endswith('@birlainstitute.co.in'):
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Generate OTP
                otp = generate_otp()

                # Save the OTP in the session for verification
                request.session['login_otp'] = otp

                # Send OTP to user's email
                send_otp_email(email, otp)

                # Redirect to OTP verification page
                return render(request, 'otp_verification.html')

            else:
                messages.error(request, error)
        else:
            messages.error(request, "Email domain not allowed.")

    return render(request, 'bonafide_details.html')


def admin_home(request):
    return render(request, 'admin_home.html')

# def admin_login_page(request):
    # return redirect('admin_home')

class CustomLoginView(LoginView):
    template_name = 'bonafide_details.html'

bonafide_details = CustomLoginView.as_view()

def bonafide_details(request):
    if request.method == 'POST':
        Name = request.POST.get('Name')
        Fathers_Name = request.POST['Fathers_Name']
        Email = request.POST["Email"]
        Department_Choice =  request.POST["Department_Choice"]
        Passing_Year = request.POST["Passing_Year"]
        Phone = request.POST["Phone"]
        University_Roll_Number = request.POST["University_Roll_Number"]
        Write_Purpose = request.POST["Write_Purpose"]
        Application_Date = request.POST['Application_Date']

        # Save data to the database
        Student.objects.create(
            Name=Name,
            Fathers_Name=Fathers_Name,
            Email=Email,
            Department_Choice=Department_Choice,
            Passing_Year=Passing_Year,
            Phone=Phone,
            University_Roll_Number=University_Roll_Number,
            Write_Purpose=Write_Purpose,
            Application_Date=Application_Date,
        )

        return redirect('base')  # Redirect to a success page after saving data

    return render(request, 'bonafide_details.html')


def base_view(request):
    return render(request, 'base.html')


def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    # Implement your email sending logic here
    # You can use Django's built-in email sending functions
    # Example using Django's send_mail:
    from django.core.mail import send_mail

    subject = 'OTP for Login'
    message = f'Your OTP for login is: {otp}'
    from_email = 'kashvijoshi1202@gmail.com'  # Replace with your email
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def verify_login_otp(request):
    if request.method == 'POST':
        submitted_otp = request.POST.get("otp")
        stored_otp = request.session.get('login_otp')

        if submitted_otp == stored_otp:
            # Clear the stored OTP from the session
            del request.session['login_otp']

            # Perform login
            # (You can redirect to the desired page or perform additional actions)
            return redirect('bonafide_details')
        else:
            messages.error(request, "Invalid OTP.")
    
    # Redirect to the login page if OTP verification fails
    return render(request, 'bonafide_details.html')  # Update the template name if needed


class STUDENTDETAILSVIEW(View):
    """
    STUDENTDETAILSVIEW class.

    Provides two methods:

    * `get()`: Renders the customer details template.
    * `post()`: Saves the customer details to the database.
    """
    def get(self, request):
        """
        Handle HTTP GET requests for the customer details view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: A rendered HTML response containing the customer details form.
        """
        form = StudentForm()
        return render(
            request, "bonafide_details.html", {"form": form}
        )

    def post(self, request):
        """
        Saves the customer details to the database.

        Args:
            request: The HTTP request object.

        Returns:
            The redirect to the customer success page.
        """
        Name = request.POST["Name"]
        Fathers_Name = request.POST["Fathers_Name"]
        Email = request.POST["Email"]
        Department_Choice =  request.POST["Department_Choice"]
        Passing_Year = request.POST["Passing_Year"]
        Phone = request.POST["Phone"]
        University_Roll_Number = request.POST["University_Roll_Number"]
        Write_Purpose = request.POST["Write_Purpose"]

        student = Student(
            Name=Name,
            Fathers_Name=Fathers_Name,
            Email=Email,
            Department_Choice=Department_Choice,
            Passing_Year=Passing_Year,
            Phone=Phone,
            University_Roll_Number=University_Roll_Number,
            Write_Purpose=Write_Purpose,
        )
        student.save()

         # Redirect to the success page based on the department
        if Department_Choice == 'computer_science':
            return redirect(reverse("computer_science_success"))
        elif Department_Choice == 'electronics_and_communication':
            return redirect(reverse("electronics_success"))
        elif Department_Choice == 'master_of_computer_application':
            return redirect(reverse("mca_success"))
        else:
            # Handle other cases or redirect to a generic success page
            return redirect(reverse("student_success"))


class ComputerScienceSuccessView(View):
    template_name = 'computer_science_success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ElectronicsSuccessView(View):
    template_name = 'electronics_success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MCASuccessView(View):
    template_name = 'mca_success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
        # return redirect(reverse("student_success"))
    

"""
  Customer_Success 
 View to render the customer success page.
 This view is used to render the "customer_success.html" template.
 It does not take any arguments and returns an HTTP response containing the rendered template.
 View class for rendering the customer success page

        Render the customer success page.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: A response containing the rendered customer success page.
        """

class STUDENTSUCCESSVIEW(View):
    def get(self, request):
        
        return render(request, "bonafide_details.html")
    

"""
 View to fetch customer data and return it as JSON.
 This view takes an HTTP GET request and returns a JSON response containing data for all customers.
     View for fetching customer data and returning it as JSON response.

     Parameters:
         request (HttpRequest): The HTTP request object.

     Returns:
         JsonResponse: A JSON response containing customer data.
        """

def student_data_view(request):
    students = Student.objects.all()
    data = [
        {
            "Name": student.Name,
            "Fathers_Name": student.Fathers_Name,
            "Email": student.Email,
            "Department_Choice": student.Department_Choice,
            "Passing_Year": student.Passing_Year,
            "Phone": student.Phone,
            "University_Roll_No": student.University_Roll_No,
            "Write_Purpose":student.Write_Purpose
        }
        for student in students
    ]
    return JsonResponse(data, safe=False)


"""
 Saving Customer REgistrations     
 View to save customer registrations.
 This view takes an HTTP POST request with form data and saves it to the database.
 It then redirects the user to the "customer_success" page.

Saves the customer registration details.

Args:
    request: The HTTP request object.

Returns:
    A redirect to the customer success page.

This function saves the customer registration details that were submitted by the user. The details include the user's full name, email address, company name, and contact information. The function then redirects the user to the customer success page.
"""

# def save_student_registrations(request):
 
#     if request.method == "POST":
        
#         fullName = request.POST.get("fullName")
#         email = request.POST.get("email")
#         company = request.POST.get("company")
#         contact = request.POST.get("contact")

#         student_registrations = Student_Registration(
#             fullName=fullName, email=email, company=company, contact=contact
#         )
#         student_registrations.save()

#         return redirect("student_success")


"""
Saving Cutsomer DEtails  
 View to save customer details.
 This view takes an HTTP POST request with form data and saves it to the database.
 It then redirects the user to the "customer_success" page.
    
    View for saving customer details.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect response to the customer success page.
    """

def save_student_details(request):
    
    if request.method == "POST":
                # Retrieve various customer details from the request
                # Extract data from the POST request
        Name = request.POST.get("Name")
        Fathers_Name = request.POST.get("Fathers_Name")
        Email = request.POST.get("Email")
        Department_Choice = request.POST.get("Department_Choice")
        Passing_Year = request.POST.get("Passing_Year")
        Phone = request.POST.get("Phone")
        University_Roll_No = request.POST.get("University_Roll_No")
        Write_Purpose = request.POST.get("Write_Purpose")
        # if "VuInfra360" in request.POST:
        #     VuInfra360 = True
        # else:
        #     VuInfra360 = False

        # option1 = VuInfra360
        # servers = request.POST.get("servers")
        # network_devices = request.POST.get("network_devices")
        # availiablity = request.POST.get("availiablity")
        # config_collectors = request.POST.get("config_collectors")
        # netflow = request.POST.get("netflow")

        # VuLogx = False
        # if "VuLogx" in request.POST:
        #     VuLogx = True
        # else:
        #     VuLogx = False
        # option2 = VuLogx
        # logs = request.POST.get("logs")

        # VuBJM = False
        # if "VuBJM" in request.POST:
        #     VuBJM = True
        # else:
        #     VuBJM = False
        # option3 = VuBJM
        # journey = request.POST.get("journey")
        # applications = request.POST.get("applications")
        # nodes = request.POST.get("nodes")
        # transactions = request.POST.get("transactions")

        # VuGeneric = False
        # if "VuGeneric" in request.POST:
        #     VuGeneric = True
        # else:
        #     VuGeneric = False
        # option4 = VuGeneric
        # users = request.POST.get("users")
        student = Student(
            Name=Name,
            Fathers_Name=Fathers_Name,
            Email=Email,
            Department_Choice=Department_Choice,
            Passing_Year=Passing_Year,
            Phone=Phone,
            University_Roll_No=University_Roll_No,
            Write_Purpose=Write_Purpose,
            # netflow=netflow,
            # option2=option2,
            # logs=logs,
            # option3=option3,
            # journey=journey,
            # applications=applications,
            # nodes=nodes,
            # transactions=transactions,
            # option4=option4,
            # users=users,
        )
                # Create and save a new Customer instance with the retrieved details
        student.save()

        return redirect("student_success")


"""
 License Details 
 View to render the license details page.
 This view takes an HTTP GET request with the "customerid" parameter.
 It retrieves the customer with the provided ID and renders the "license_details.html" template with the customer data.

    View for rendering license details page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the rendered license details page or an error page if the customer does not exist.
    """

# def bonafide_details(request):
#     student_id = request.GET.get("studentid", 0)
#     try:
#         student = Student.objects.get(id=student_id)
#         context = {"student": student}
#         return render(request, "bonafide_details.html", context)

#     except Student.DoesNotExist:
#         return render(request, "error.html", {"message": "Student not found"})


"""
 Customer Registration Page 
 View to render the customer registration page.
 This view is used to render the "customer_registration.html" template.
 It does not take any arguments and returns an HTTP response containing the rendered template.

    View for rendering customer registration page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the rendered customer registration page.
    """

def studentr_registration(request):
    return render(request, "/student_registration.html")


"""
Calling API 
    
    View for approving customer requests.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A success response message.
    """

def approve_request(request):
    studentid= request.GET.get('id')
    status= request.GET.get('status')
    try:
        # Fetch the customer based on the provided customer_id
        student = Student.objects.get(id=studentid)
    

        
        student.application_status = status

        # Save the updated customer details back to the database
        student.save()

        return HttpResponse("Status Updated")
    
    
    except Student.DoesNotExist:
        return HttpResponse("Student not found.", status=404)

    # Assuming 'status' is a field in the Customer model, update the customer's status
        



"""
  Login Page 
 this login view is used for logging in to the interface 
 THe authentication is done on the basis of username and password 
 You need to select the role and then enter your username and password and if you are authenticated user you'll be logged into the home pages on the basis of your role. 
 View to handle the login process.
 This view takes an HTTP POST request with login credentials (role, username, and password).
 It authenticates the user and redirects them to the appropriate home page based on their role.
    
    View for user authentication and login.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect response based on user role or an error page for invalid credentials.
    """

# def login_view(request):
#     if request.method == "POST":
#         # role = request.POST.get("role")
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         error = "error Invalid credentials"
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)

#             # if role == "associate":
#                 # return redirect("/associate/home/")
#             if role == "admin":
#                 return redirect("/admin/home/")  # Redirect to the approver home page
#             elif role == "student":
#                 student_list = Student_Registration.objects.all()
#                 return render(
#                     request,
#                     ("student_home.html"),
#                     {"student_list": student_list},
#                 )  # Redirect to the manager home page
#             else:
#                 # Handle invalid role
#                 return render(request, "error.html")
#         else:
#             # Authentication failed, display error message or redirect to login page
#             return render(request, "error.html")
#     else:
#         error = ""
#         return redirect(reverse(error))


"""
 Logout View
 This view logs out the user and redirects them to the "base" page.
    
    View to handle user logout.

    Arguments:
        request (HttpRequest): The HTTP POST request.

    Returns:
        HttpResponseRedirect: Redirects to the "base" page after logout.
    """

def logout_view(request):

    # Redirect to the appropriate page after logout
    return redirect("base")  


"""
 Associate Home Page
 View to render the associate home page.
 This view retrieves a list of all customer registrations and renders the "associate_home.html" template.
    
    View to render the associate home page.

    Arguments:
        request (HttpRequest): The HTTP GET request.

    Returns:
        HttpResponse: Response containing the rendered template.
    """

# def associate_home_view(request):
#     # Logic for the associate home page
#     customer_list = Customer_Registration.objects.all()
#     return render(
#         request,
#         "licenseManagement/associate_home.html",
#         {"customer_list": customer_list},
#     )


"""
 Approver Home Page 
 View to render the approver home page.
 This view retrieves a list of all customers and renders the "approver_home.html" template.
    
    View to render the approver home page.

    Arguments:
        request (HttpRequest): The HTTP GET request.

    Returns:
        HttpResponse: Response containing the rendered template.
    """

def admin_home_view(request):
    # Logic for the approver home page
    request_list = Student.objects.all()
    return render(
        request,
        "admin_home.html",
        {"request_list": request_list},
    )


