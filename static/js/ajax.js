$('#btn').click(function (){
        $.ajax({
            url:"{% url 'index' %}",
            type: 'post',
            data:{
                uname:$('#username').val(),
                pw:$('#password').val(),
                csrfmiddlewaretoken:$('[name=csrfmiddlewaretoken]').val(),
            },
            success:function (res){
                var resStr = JSON.parse(res);
                if (resStr['code'] === 3){
                    var spanEle = document.createElement('span');
                    $(spanEle).text(resStr['redirect_url'])
                    $('form').append(spanEle)
                }
                else if(resStr['code'] === 0){
                    location.href=resStr['redirect_url']
                }
                console.log(res);
            }
        })
    })