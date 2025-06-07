import cx_Oracle
from django.shortcuts import render, redirect
from .forms import ComplaintForm,ApplicationForm
from django.http import FileResponse
from django.db import connection
from django.contrib.auth.decorators import login_required

def lodge_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user.student
            complaint.save()
            return redirect('homepage')
    else:
        form = ComplaintForm()
    return render(request, 'hostel/lodge_complaint.html', {'form': form})


def download_voucher(request):
    file = open('static/fee_voucher.pdf', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename="FeeVoucher.pdf"'
    return response


def submit_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():

            application = form.save(commit=False)
            application.applicant = request.user.student
            application.save()
            return redirect('homepage')
    else:
        form = ApplicationForm()
    return render(request, 'hostel/room_application.html', {'form': form})

@login_required
def fetch_complaints(request):
    cursor = connection.cursor()

    # Define a PL/SQL anonymous block
    plsql = """
        DECLARE
            complaints_cursor SYS_REFCURSOR;
        BEGIN
            get_all_complaints(complaints_cursor);  -- Call the stored procedure
            :complaints := complaints_cursor;  -- Fetch the results into a bind variable
        END;
        """

    # Define a bind variable
    complaints_var = cursor.var(cx_Oracle.CURSOR)

    # Execute the PL/SQL block with the bind variable
    cursor.execute(plsql, {'complaints': complaints_var})

    # Fetch all rows
    rows = complaints_var.getvalue().fetchall()

    return render(request, 'hostel/complaints.html', {'complaints': rows})

def fetch_applications(request):
    cursor = connection.cursor()

    # Define a PL/SQL anonymous block
    plsql = """
        DECLARE
            applications_cursor SYS_REFCURSOR;
        BEGIN
            fetch_applications(applications_cursor);  -- Call the stored procedure
            :applications := applications_cursor;  -- Fetch the results into a bind variable
        END;
        """

    # Define a bind variable
    applications_var = cursor.var(cx_Oracle.CURSOR)

    # Execute the PL/SQL block with the bind variable
    cursor.execute(plsql, {'applications': applications_var})

    # Fetch all rows
    rows = applications_var.getvalue().fetchall()
    print(rows)

    return render(request, 'hostel/applications.html', {'applications': rows})
