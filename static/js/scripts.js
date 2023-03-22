/***
 * JOBS RELATED
 */

// Add job from form data
$("#add_job_form").on("submit", function(){
    // Get form data from HTML form
    
    var url = '/run_job';
    var data = {
        'job_name': $("#job_name").val(),
        'image': $("#job_image").val(),
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Job " + data.job_name + " has been started");
            window.location.reload();
        }
    });
    return false;
});


// Runs job again based on image_id and job_name
function run_job(job_name, image_id) {
    if (window.event.target.classList.contains("fa-redo")) {
        window.event.target.classList.remove("fa-redo");
        window.event.target.classList.add("fa-spinner");
        window.event.target.classList.add("fa-spin");
    } else {
        window.event.target.children[0].classList.remove("fa-redo");
        window.event.target.children[0].classList.add("fa-spinner");
        window.event.target.children[0].classList.add("fa-spin");
    }
    var url = '/run_job';
    var data = {
        'job_name': job_name.substring(0, job_name.length-9), // Remove last 9 characters from the job name
        'image': image_id
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Job " + data.job_name + " has been started");
            window.location.reload();
        }
    });
}

// Removes job based on job_name
function remove_job(job_name, retry_as_service=true) {
    if (window.event.target.classList.contains("fa-trash")) {
        window.event.target.classList.remove("fa-trash");
        window.event.target.classList.add("fa-spinner");
        window.event.target.classList.add("fa-spin");
    } else {
        window.event.target.children[0].classList.remove("fa-trash");
        window.event.target.children[0].classList.add("fa-spinner");
        window.event.target.children[0].classList.add("fa-spin");
    }
    const thiz = this;
    var url = '/remove_job';
    var data = {
        'job_name': job_name
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Job " + data.job_name + " has been removed");
            window.location.reload();
        },
        error: function () {
            if (retry_as_service) {
                thiz.remove_service(job_name, false);
            } else {
                window.alert("Service or Job " + job_name + " could not be removed");
                window.location.reload();
            }
        }
    });
}

/***
 * SERVICES RELATED
 */


// Add job from form data
$("#add_service_form").on("submit", function(){
    // Get form data from HTML form
    var url = '/add_service';
    var data = {
        'service_name': $("#service_name").val(),
        'image': $("#service_image").val(),
    };

    console.log(data);

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Service " + data.service_name + " has been started");
            window.location.reload();
        }
    });
    return false;
});

// Updates a service's replicas
function update_replicas(service_name, replicas) {
    var url = '/scale_service';
    var data = {
        'service_name': service_name,
        'replicas': replicas
    };

    $.ajax({
        url: url,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Service " + data.service_name + " has been updated with " + data.replicas + " replicas.");
            window.location.reload();
        }
    });
}

function remove_service(service_name, retry_as_job=true) {
    if (window.event.target.classList.contains("fa-trash")) {
        window.event.target.classList.remove("fa-trash");
        window.event.target.classList.add("fa-spinner");
        window.event.target.classList.add("fa-spin");
    } else {
        window.event.target.children[0].classList.remove("fa-trash");
        window.event.target.children[0].classList.add("fa-spinner");
        window.event.target.children[0].classList.add("fa-spin");
    }
    const thiz = this;
    var url = '/remove_service';
    var data = {
        'service_name': service_name
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Service " + data.service_name + " has been removed");
            window.location.reload();
        },
        error: function () {
            if (retry_as_job) {
                thiz.remove_job(service_name, false);
            } else {
                window.alert("Service or Job " + service_name + " could not be removed");
                window.location.reload();
            }
        }
    });
}