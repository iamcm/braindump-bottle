var EventRegistry = []

var Router = {
    showPage:function(id){
        $('.page').hide();
        $('#'+ id).show();

        /*$('.nav li').removeClass('active');
        var li = $('#'+ id).data('active-menu-item');
        $('#'+ li).addClass('active');*/
    }

}

var Tag = {

    getAllRaw:function(callback){
        var self = this;

        $.getJSON('/api/tags', function(json){
            if(callback) callback(json);
        })
    },

    getAll:function(callback){
        var self = this;

        $.getJSON('/api/tags', function(json){
            Util.Templating.renderTemplate('tagsTpl', {'tags':json}, 'tags');

            if(callback) callback();
        })
    },

    getAllAdmin:function(callback){
        var self = this;

        $.getJSON('/api/tags', function(json){
            Util.Templating.renderTemplate('tagsAdminTpl', {'tags':json}, 'tagsAdmin');

            if(callback) callback();
        })
    },

    renderForm:function(id){
        if(!id){
            Util.Templating.renderTemplate('formTagTpl', {}, 'formTag');
        } else {
            $.getJSON('/api/tag/'+ id, function(json){
                Util.Templating.renderTemplate('formTagTpl', json, 'formTag');
            })
        }

    },

    save:function(params, callback){
        params = Util.querystringToObject(params);
        
        var url = '/api/tag';

        if(params['_id']){
            url += '/api/'+ params['_id'];
        }

        $.post(url, params, function(){
            if(callback) callback();
        })
    },

    delete:function(id, callback){
        $.post('/api/tag/'+id+'/delete', function(){
            if(callback) callback();
        })
    },

    attachEvents:function(){
        var self = this;

        if(EventRegistry.indexOf("formAddTag") == -1){            
            EventRegistry.push('formAddTag');

            $('#formAddTag').live('submit', function(ev){
                ev.preventDefault();

                var params = $(this).serialize();

                self.save(params, function(){
                    window.location = '/index.html';
                });

            })
        }
    }
}

var Item = {

    getAll:function(tagname, callback){
        var self = this;

        $.getJSON('/api/items?tag='+ tagname, function(json){
            Util.Templating.renderTemplate('itemsTpl', {'items':json}, 'items');

            if($('#items').children().length==1){
                $('.content').show();                    
            }

            if(callback) callback();
        })
    },

    renderForm:function(id){

        Tag.getAllRaw(function(jsonTags){
           if(!id){
                Util.Templating.renderTemplate('formItemTpl', {'tags':jsonTags}, 'formItem');

                tinyMCEInit();
            } else {
                $.getJSON('/api/item/'+ id, function(json){
                    $.each(jsonTags, function(i, el){
                        if(json.tagIds.indexOf(el._id) != -1){
                            el['selected'] = true;
                        }
                    });
                    json['tags'] = jsonTags;
                    Util.Templating.renderTemplate('formItemTpl', json, 'formItem');

                    tinyMCEInit();
                })
            }
        });



    },

    save:function(params, callback){
        _params = Util.querystringToObject(params);
        
        params['tagIds[]'] = [];
        $('.tag.btn-primary').each(function(){
            params += "&tagIds[]=" + this.id;
        });

        var url = '/api/item';

        if(_params['_id']){
            url += '/'+ _params['_id'];
        }

        $.post(url, params, function(){
            if(callback) callback();
        })
    },

    delete:function(id, callback){
        $.post('/api/item/'+id+'/delete', function(){
            if(callback) callback();
        })
    },

    attachEvents:function(){
        var self = this;

        if(EventRegistry.indexOf("formAddItem") == -1){            
            EventRegistry.push('formAddItem');

            $('#formAddItem').live('submit', function(ev){
                ev.preventDefault();

                var params = $(this).serialize();

                self.save(params, function(){
                    window.location = '/index.html';
                });

            })
        }

        if(EventRegistry.indexOf(".item .title") == -1){            
            EventRegistry.push('.item .title');

            $('.item .title').live('click', function(){
                var content = $(this).next();
                $(content).toggle();
            });
        }

        if(EventRegistry.indexOf(".item .content a") == -1){            
            EventRegistry.push('.item .content a');

            $('.item .content a').live('click', function(){
                ev.preventDefault();
                window.open(this.href);
            });
        }

        if(EventRegistry.indexOf("#formAddItem .tag") == -1){            
            EventRegistry.push('#formAddItem .tag');

            $('#formAddItem .tag').live('click', function(ev){
                ev.preventDefault();
                $(this).toggleClass('btn-primary');
            });
        }
    }
}

var Search = {

    getAll:function(searchterm, callback){
        var self = this;

        $.getJSON('/api/search/'+ searchterm, function(json){
            Util.Templating.renderTemplate('itemsTpl', {'items':json}, 'items');

            if($('#items').children().length==1){
                $('.content').show();                    
            }

            if(callback) callback();
        })
    },

    attachEvents:function(){
        var self = this;

        if(EventRegistry.indexOf("search") == -1){            
            EventRegistry.push('search');

            $('#search').focus().keyup(function(){
                if(this.value==''){
                    $('#items').html('');
                } else {
                    self.getAll(this.value);
                }
            });
        }
    }
}

var ApiKey = {

    get:function(callback){
        var self = this;

        $.get('/api/apikey').done(function(key){
            if(callback) callback(key);
        });
    },

    generateKey:function(callback){
        var self = this;

        $.post('/api/apikey').done(function(key){
            if(callback) callback(key);
        });
    },

    attachEvents:function(){
        var self = this;

        if(EventRegistry.indexOf("btnGenerateApiKey") == -1){            
            EventRegistry.push('btnGenerateApiKey');

            $('#btnGenerateApiKey').live('click', function(){
                self.generateKey(function(key){
                    $('#apiKeyContainer').text(key);
                })
            });
        }
    }
}


$(document).ajaxError(function(event, jqxhr){
    if(jqxhr.status == 403){
        window.location = '/login.html';
    } else {
        Util.flashMessage('error', 'An error has occured');
    }
})

function watchDeleteClicks(){
    $('.deleteLink').live('click', function(){
        return confirm('Are you sure you want to delete this '+ $(this).attr('entity'))
    })  
}

$(document).ready(function(){
    watchDeleteClicks();
    Tag.getAll();
    Search.attachEvents();
    Item.attachEvents();
    Tag.attachEvents();
});

Path.map("#/").to(function(){
    Router.showPage('pageHome');
    Tag.getAll();
});

Path.map("#/tags").to(function(){
    Router.showPage('pageTags');
    Tag.getAllAdmin();
});

Path.map("#/tag").to(function(){
    Router.showPage('pageTag');
    Tag.renderForm();
});

Path.map("#/tag/:id").to(function(){
    Router.showPage('pageTag');
    Tag.renderForm(this.params['id']);
});

Path.map("#/tag/:id/delete").to(function(){
    Tag.delete(this.params['id'], function(){
        window.location = '/index.html';
    });
});

Path.map("#/item").to(function(){
    Router.showPage('pageItem');
    Item.renderForm();
});

Path.map("#/item/:id").to(function(){
    Router.showPage('pageItem');
    Item.renderForm(this.params['id']);
});

Path.map("#/item/:id/delete").to(function(){
    Item.delete(this.params['id'], function(){
        window.location = '/index.html';
    });
});

Path.map("#/filter/tag/:tagname").to(function(){
    Router.showPage('pageHome');
    Item.getAll(this.params['tagname'])
});

Path.map("#/api-key").to(function(){
    Router.showPage('pageApiKey');
    ApiKey.attachEvents();
    ApiKey.get(function(key){
        $('#apiKeyContainer').text(key);
    })
});


Path.root("#/");

Path.listen();
