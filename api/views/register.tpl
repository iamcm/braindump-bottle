
<div class="container-fluid p10">
    
    %if vd.get('error'):
    <div class="alert alert-error">
        <button class="close" data-dismiss="alert">×</button>
        {{vd['error']}}
    </div>
    %end

    <form class="form-horizontal" id="registerForm" method='POST' action="" >
        
        <div class="control-group">
            <label class="control-label" for="email">Email</label>
            <div class="controls">
                <input type="text" class="input-xlarge" name="email" id="email" value="{{vd.get('email') if vd.get('email') else ''}}" />
            </div>
        </div>
        
        <div class="control-group">
            <label class="control-label" for="password1">Password</label>
            <div class="controls">
                <input type="password" class="input-xlarge" name="password1" id="password1" value="{{vd.get('password1') if vd.get('password1') else ''}}" />
            </div>
        </div>
        
        <div class="control-group">
            <label class="control-label" for="password2">Password again</label>
            <div class="controls">
                <input type="password" class="input-xlarge" name="password2" id="password2" value="{{vd.get('password2') if vd.get('password2') else ''}}" />
            </div>
        </div>
        
        <div class="control-group">
            <div class="controls">
                <button type="submit" class="btn">Create account</button>
            </div>
        </div>
        
    </form>
</div>

%rebase base_public