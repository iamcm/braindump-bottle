
<div class="container-fluid p10">
    
    %if vd.get('error'):
    <div class="alert alert-error">
        <button class="close" data-dismiss="alert">×</button>
        {{vd['error']}}
    </div>
    %end

    <form class="form-horizontal" id="loginForm" method='POST' action="/login" >
        
        <div class="control-group">
            <div class="controls">
                <input type="text" class="input-xlarge" name="email" id="email" value="{{vd.get('email') if vd.get('email') else ''}}" placeholder="Email" />
            </div>
        </div>
        
        <div class="control-group">
            <div class="controls">
                <input type="password" class="input-xlarge" name="password" id="password" value="{{vd.get('password') if vd.get('password') else ''}}" placeholder="Password" />
            </div>
        </div>
        
        <div class="control-group">
            <div class="controls">
                <button type="submit" class="btn">Login</button>
            </div>
        </div>
        
    </form>
</div>

%rebase base_public