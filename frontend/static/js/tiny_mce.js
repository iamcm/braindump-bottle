function tinyMCEInit(){
    tinyMCE.init({
        mode : "textareas",
        theme : "advanced",
        height: '200',
        width: '700',
        content_css : "/static/css/tiny_mce.css",

        theme_advanced_buttons1 : "bold,italic,underline,|,bullist,numlist,link,|,styleselect, fontselect, fontsizeselect,|,forecolor,backcolor",
        theme_advanced_buttons2 : "",
        theme_advanced_buttons3 : "",
        theme_advanced_buttons4 : "",
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_resizing : true,
        style_formats : [                                                
            {title : 'Heading', inline : 'span', styles : {fontSize:'120%',fontWeight:'bold',marginBottom:'5px'}},  
            {title : 'Indent', inline : 'span', styles : {marginLeft:'2%',marginRight:"2%"}},
            {title : 'Code', inline : 'span', styles : {fontFamily:'courier new'}}
        ]
    });
};

$(document).ready(function(){
    tinyMCEInit();
});