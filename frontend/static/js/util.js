Util = {
    querystringToObject:function(querystring){
        var outputobj = {};
        var querystringparts = querystring.split('&');
        for(i in querystringparts){
            var parts = querystringparts[i].split('=');

            outputobj[parts[0]] = parts[1];
        }

        return outputobj;
    },

    printPage:function(classname){
        $('body').addClass(classname);
        window.print();
        $('body').removeClass(classname);
    },

    /**
    * show a message at the top of the screen on a coloured background 
    * based on the message type.
    * Standard bootstrap messagetypes are used:
    *   alert, error, success, info 
    * e.g.
    *   Utility.flashMessage('error', 'An error has occured');
    */
    flashMessage: function (messagetype, message) {

        var html = '<div class="alert alert-' + messagetype + '">';
        html += '<button type="button" class="close" data-dismiss="alert">&times;</button>';
        html += message + '</div>'

        if($('#flashmessagecontent').length<1){
            var content = Util.Html.div({id:'flashmessagecontent'});
            var container = Util.Html.div({id:'flashmessagecontainer', content:content});

            $('body').append(container);
        }

        $('#flashmessagecontent').html(html);

        setTimeout(function(){
            if($('#flashmessagecontent')) $('#flashmessagecontent').fadeOut(function(){
                $(this).html('').show();
            });
        },7000)
    },

    removeFlashMessage: function(){
        $('#flashmessagecontent').html('');  
    }
}

Util.Html = {

    /**
     * obj.content
     * obj.id
     * obj.classname
     * obj.style
     */
    div:function(obj){
        
        var id = (obj.id) ? ' id="'+ obj.id +'"' : '' ;
        var classname = (obj.classname) ? ' class="'+ obj.classname +'"' : '' ;
        var style = (obj.style) ? ' style="'+ obj.style +'"' : '' ;
        
        return '<div'+ id + classname + style +'>'+ obj.content +'</div>';
        
    },
    
    /**
     * obj.content
     * obj.id
     * obj.classname
     * obj.style
     * obj.title
     */
    span:function(obj){
        
        var id = (obj.id) ? ' id="'+ obj.id +'"' : '' ;
        var classname = (obj.classname) ? ' class="'+ obj.classname +'"' : '' ;
        var style = (obj.style) ? ' style="'+ obj.style +'"' : '' ;
        var title = (obj.title) ? ' title="'+ obj.title +'"' : '' ;
        
        return '<span'+ id + classname + style + title +'>'+ obj.content +'</span>';
    },

    /**
     * obj.content = [{object},{object},{object}]
     * obj.id
     * obj.classname
     * obj.style
     * obj.name
     * obj.valueKey
     * obj.nameKey
     * eg: 
        var items = [{"userId": "517eccc56e95525724fc10c6", "name": "collection 1", "_id": "517eda086e95525e8b990aab"}, {"userId": "517eccc56e95525724fc10c6", "name": "collection 2", "_id": "517eda2d6e95525e8b990aac"}]
        
        var html = Util.Html.select({
                name:'dropCollections',
                content:items,
                valueKey:'_id',
                nameKey:'name',
            });
     */
    select:function(obj){
        var id = (obj.id) ? ' id="'+ obj.id +'"' : '' ;
        var classname = (obj.classname) ? ' class="'+ obj.classname +'"' : '' ;
        var style = (obj.style) ? ' style="'+ obj.style +'"' : '' ;
        var name = (obj.name) ? ' name="'+ obj.name +'"' : '' ;

        var options = ''
        $.each(obj.content, function(i, el){
            options += '<option value="'+ el[obj.valueKey] +'">'+ el[obj.nameKey] +'</option>'
        })

        return '<select '+ id + classname + style + name +'>'+ options +'</select>';
    }  
}

Util.String = {
    trim:function(string, maxlength, addTitle){       
        if(string.length > length){
            var output = string.slice(0, maxlength) + '...';
            
            if(addTitle){
                output = Util.Html.span({
                    'content':output,
                    'title':string
                })
            }
        } else {
            var output = string;
        }   
        
        return output;
    }
}

Util.Templating = {
    renderTemplate:function(templateid, context, targetid, fadeInEl){
        var source = $('#'+ templateid).html();
        var template = new t(source);
        $('#'+ targetid).html(template.render(context));
        if(fadeInEl) $(fadeInEl).fadeIn(50);
    }
}