// Login Request
$(document).on('submit', '#login-form', function(e){

    e.preventDefault();


    let login_btn = document.querySelector('.login-btn')

    // Login btn React on submit

    login_btn.disabled =  true
    login_btn.style.cursor = 'progress'
    login_btn.style.opacity = '.8'

    var form_data = new FormData(document.getElementById('login-form'));
    $('#error-message').html('')


    // Sending Request
    let req = $.ajax({
        type:'post',
        url:'/auth/login/',
        data: form_data,
        cache: false,
        processData: false,
        contentType: false,
    });
    setTimeout(() => {login_btn.innerHTML = 'Logging in . .' }, 300);

    // On success
    req.done(function(data){
        console.log(data)
        if (data['success']){
            // reinitializing login button

            setTimeout(() => {login_btn.innerHTML = 'Redirecting' }, 200);
            login_btn.innerHTML = 'Login'

            // Redirecting

            window.location.href = redirect_url

        }
        else {
            // If Account not found , show some alert on the window and reset the buttons
            login_btn.innerHTML = 'Login'
            $('#error-message').html('No account found with given credentials!')
            login_btn.disabled = false
            login_btn.style.cursor = 'pointer'

        }

    })

})

// Register Request
$(document).on('submit', '#register-form', function(e){

    console.log("come here")

    e.preventDefault();

    if ($('#pass1').val() !== $('#pass2')){

        $('#error-message').html("Password didn't match!")
        return
    }

    let redirect_url;
    let register_btn = document.querySelector('.register-btn')

    // Login btn React on submit

    register_btn.disabled =  true
    register_btn.style.cursor = 'progress'
    register_btn.style.opacity = '.8'

    var form_data = new FormData(document.getElementById('register-form'));


    // Sending Request
    let req = $.ajax({
        type:'post',
        url:'/auth/register/',
        data: form_data,
        cache: false,
        processData: false,
        contentType: false,
    });
    setTimeout(() => {register_btn.innerHTML = 'Registering . .' }, 300);

    // On success
    req.done(function(data){

        if (data['success']){
            // reinitializing register button

            setTimeout(() => {register_btn.innerHTML = 'Redirecting' }, 200);
            register_btn.innerHTML = 'Register'

            // Redirecting

            window.location.href = data['redirect']

        }
        else {
            // If something went wrong , show some alert on the window and reset the buttons
            register_btn.innerHTML = 'Register'

            register_btn.disabled = false
            register_btn.style.cursor = 'pointer'

        }

    })

})