$(function(){
	$('.addcategory').click(function(){      //增加类别
		$('.addcategory-form').toggle();
		if($(this).hasClass('glyphicon-plus')){
			$(this).removeClass('glyphicon-plus');
			$(this).addClass('glyphicon-minus');
		}else{
			$(this).removeClass('glyphicon-minus');
			$(this).addClass('glyphicon-plus');
		}
		$('.message').hide();
	});
	$('#addcategorysumit').click(function(){  //提交表单
		$('.message').removeClass('alert-danger');
        $('.message>strong').text('');
        $('.message').hide();
        catname = $('#addcategory-form input[name="cat_name"]').val();
        if(catname == ''){
        	$('.addcategory-form').toggle();
        	$('.addcategory').removeClass('glyphicon-minus');
			$('.addcategory').addClass('glyphicon-plus');
        	$('.message').addClass('alert-danger');
            $('.message>strong').text('请填写分类名称');
            $('.message').show();
            return;
        }
		$.ajax({
            cache: true,
            type: "POST",
            url:"/by/admin",
            data:$('#addcategory-form').serialize(),
            error: function() {
            	$('.message').addClass('alert-danger');
                $('.message>strong').text('网络错误');
            },
            success: function(data) {
            	if(data == '增加成功'){
            		window.location.reload();
            	}else{
            		$('.addcategory-form').toggle();
                	$('.addcategory').removeClass('glyphicon-minus');
        			$('.addcategory').addClass('glyphicon-plus');
	            	$('.message').addClass('alert-danger');
	                $('.message>strong').text(data);
	                $('.message').show();
            	}
            }
        });
	});
	$('#submit-postarticle').click(function(e){   //发布文章
		var flag = false;
		e.preventDefault();
		if(!ue.hasContents()){
            $('.message>strong').text('文章内容为空');
            flag = true;
		}
		if($("#article input[name='title']").val() == ''){
			$('.message>strong').text('标题为空');
			flag = true;
		}
		if($("#article input[name='shortdesc']").val() == ''){
			$('.message>strong').text('导读为空');
			flag = true;
		}
		if($("#postarticle select[name='category']").val() == ''){
			$('.message>strong').text('请选择文章分类');
			flag = true;
		}
		if($("#postarticle select[name='auth']").val() == ''){
			$('.message>strong').text('请选择文章权限');
			flag = true;
		}
		if(flag){
			$('.message').addClass('alert-danger');
	        $('.message').show();
			return;
		}
		data  = $('#postarticle').serialize();
		data2 = $("#article input[name='title']").val();
		data3 = ue.getContent();
		data4 = $("#article input[name='shortdesc']").val();
		$.ajax({
            cache: true,
            type: "POST",
            url:"/by/write",
            data:data+'&title='+data2+'&content='+data3+'&shortdesc='+data4,
            async: false,
            error: function() {
            	$('.message').addClass('alert-danger');
                $('.message>strong').text('网络错误');
                $('.message').show();
            },
            success: function(data) {
            	if(data == '发表成功'){
	                window.location.href="/by/admin";
            	}else{
	            	$('.message').addClass('alert-danger');
	                $('.message>strong').text(data);
	                $('.message').show(); 
            	}
            }
        });
	});
	$('#submit-modifyarticle').click(function(e){   //修改文章
		e.preventDefault();
		flag = false;
		if(!ue.hasContents()){
            $('.message>strong').text('文章内容为空');
            flag = true;
		}
		if($("#modifyarticle input[name='title']").val() == ''){
			$('.message>strong').text('标题为空');
			flag = true;
		}
		if($("#modifyarticle input[name='shortdesc']").val() == ''){
			$('.message>strong').text('导读为空');
			flag = true;
		}
		if(flag){
			$('.message').addClass('alert-danger');
	        $('.message').show();
			return;
		}
		data  = $('#modifyarticleform').serialize();
		data2 = $("#modifyarticle input[name='title']").val();
		data3 = ue.getContent();
		data4 = $("#modifyarticle input[name='shortdesc']").val();
		aid   = $('#modifyarticleform input[name="aid"]').val();
		$.ajax({
            cache: true,
            type: "POST",
            url:"/by/modify/"+parseInt(aid),
            data:data+'&title='+data2+'&content='+data3+'&shortdesc='+data4,
            async: false,
            error: function() {
            	$('.message').addClass('alert-danger');
                $('.message>strong').text('网络错误');
            },
            success: function(data) {
            	if(data == '修改成功'){
            		$('.message').addClass('alert-info');
	                $('.message>strong').text(data);
            	}else{
	            	$('.message').addClass('alert-danger');
	                $('.message>strong').text(data);
            	}
            }
        });
        $('.message').show(); 
	});
})