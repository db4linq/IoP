(function(){var e,a,i,n,t,l,o,s,d,r,c,u,p,g,v,m;r=function(e){var a;return console.log("TEST!"),a=$.ajax({url:"/get/notification/message/names",method:"POST",data:{}}),a.done(function(a){var i,n,t,l,o,s;for(a=JSON.parse(a),console.log(a),$(".dropdown.notification_message > .menu").emtpy,i=0,n=a.length;i<n;i++)t=a[i],s=t.uuid,l=t.name,o="<div class='item' data-value='"+s+"'>"+l+"</div>",console.log(o),$(".dropdown.notification_message > .menu").append(o);return e("finished")})},window.get_notification_messages=r,l=function(e){var a;void 0!==e&&($(e).addClass("disabled"),$(e).addClass("loading")),a=$.ajax({url:"/get/plant/notification/message",method:"POST"}),a.done(function(a){if(a=JSON.parse(a),$(".notification_message_content").val(a.message),$(".ui.selection.dropdown").dropdown("set selected",a.uuid),void 0!==e)return $(e).removeClass("disabled"),$(e).removeClass("loading")})},window.get_current_notification_message=l,d=function(e){var a;return a=$.ajax({url:"/get/notification/message/content",method:"POST",data:{uuid:e}}),a.done(function(e){return e=JSON.parse(e),$(".notification_message_content").val(e)})},window.get_notification_message_content=d,m=function(e,a,i,n,t){var l,o;return null==t&&(t=!0),$(e).addClass("disabled"),$(e).addClass("loading"),l={message:a,name:i},l.responsible=t,n===!0&&(l.uuid=n),o=$.ajax({url:"/submit/notification/message",method:"POST",data:l}),o.done(function(a){return a=JSON.parse(a),"ok"!==a.code&&($(".alert").html=a.code),$(e).removeClass("disabled"),$(e).removeClass("loading")})},window.submit_notification_message=m,s=function(){var e;return e=$.ajax({url:"/get/responsibles",method:"POST"}),e.done(function(e){var a,i,n,t,l,o;for(e=JSON.parse(e),$(".ui.middle.aligned.divided.list").html(""),l=[],a=0,i=e.length;a<i;a++)n=e[a],o='<div class="item"> <div class="right floated content"> <div class="ui small basic icon buttons"> <button class="ui button"> <div class="ui radio checkbox"> <input type="radio" name="wizard" [[checked]] onChange="change_wizard_general_settings_responsible(this, \'[[identifier]]\')"> <label><i class="wizard icon"></i> </label> </div> </button> <button onclick="$(\'.[[identifier]]\').accordion(\'toggle\', 0);" class="ui button"><i class="edit icon"></i> </button> <button class="ui button" onclick="delete_general_settings_responsible(\'[[identifier]]\')"><i class="remove icon"></i> </button> </div> </div><img src="https://source.unsplash.com/category/nature" class="ui avatar image"> <div class="content">[[name]]</div> <div class="ui accordion [[identifier]]"> <div style="height:0;padding:0" class="title"></div> <div style="margin-top:1%" class="content"> <div class="ui grid"> <div class="two column row relaxed"> <div style="margin-bottom:1%" class="column"> <div class="ui fluid left icon input"> <input type="text" class="name-[[identifier]]" placeholder="Name" value="[[name]]"><i class="tag icon"></i> </div> </div> <div class="column"> <div class="ui fluid left icon input"> <input type="text" class="email-[[identifier]]" placeholder="EMail" value="[[email]]"><i class="mail icon"></i> </div> </div> </div> </div> <div class="ui two buttons"> <div class="ui basic button fluid green" onclick="change_information_general_settings_responsible(this, \'[[identifier]]\')">Apply</div> <div class="ui basic button fluid red">Reset</div> </div> </div> </div> <script type="text/javascript"> </script> </div>',o=o.replace(/\[\[identifier\]\]/g,n.uuid),o=o.replace(/\[\[name\]\]/g,n.name),o=o.replace(/\[\[email\]\]/g,n.email),t=n.wizard===!1?"":"checked",o=o.replace(/\[\[checked\]\]/g,t),l.push($(".ui.middle.aligned.divided.list").append(o));return l})},window.get_general_settings_responsibles=s,t=function(e){var a;a=$.ajax({url:"/remove/responsible",method:"POST",data:{uuid:e}}),a.done(function(e){e=JSON.parse(e),console.log(e),s()})},window.delete_general_settings_responsible=t,i=function(e,a){var i;e.checked&&(i=$.ajax({url:"/change/responsible/wizard",method:"POST",data:{uuid:a}}),i.done(function(e){e=JSON.parse(e),console.log(e),s()}))},window.change_wizard_general_settings_responsible=i,e=function(e,a){var i,n,t;$(e).addClass("disabled"),$(e).addClass("loading"),n=$(".name-"+a).val(),i=$(".email-"+a).val(),t=$.ajax({url:"/change/responsible",method:"POST",data:{uuid:a,name:n,email:i}}),t.done(function(a){a=JSON.parse(a),console.log(a),$(e).removeClass("disabled"),$(e).removeClass("loading"),s()})},window.change_information_general_settings_responsible=e,n=function(){var e,a,i;a=$(".new.name").val(),e=$(".new.email").val(),i=$.ajax({url:"/create/responsible/none",method:"POST",data:{name:a,email:e,wizard:"no"}}),i.done(function(e){return e=JSON.parse(e),console.log(e),$(".new.name").val(""),$(".new.email").val(""),s()})},window.create_new_general_settings_responsible=n,v=function(e){var a;$(e).addClass("disabled"),$(e).addClass("loading"),a=$.ajax({url:"/change/plant/intervals",method:"POST",data:{notification:$("#flat-slider-general-interval").slider("option","value"),connection:$("#flat-slider-dead-interval").slider("option","value"),non_persistant:$("#flat-slider-non-persistant-interval").slider("option","value")}}),a.done(function(a){return a=JSON.parse(a),$(e).removeClass("disabled"),$(e).removeClass("loading")})},window.modify_plant_durations=v,o=function(){var e;e=$.ajax({url:"/get/day_night",method:"POST"}),e.done(function(e){var a,i;return e=JSON.parse(e),e.ledbar&&$(".field.ledbar > .ui.checkbox > input").prop("checked",!0),e.display&&$(".field.display > .ui.checkbox > input").prop("checked",!0),e.generalleds&&$(".field.generalleds > .ui.checkbox > input").prop("checked",!0),e.notification&&$(".field.notification > .ui.checkbox > input").prop("checked",!0),a=e.start.toString(),a=3===a.length?a.slice(0,1):a.slice(0,2),i=e.stop.toString(),i=3===i.length?i.slice(0,1):i.slice(0,2),$("#flat-slider-time-interval").slider({max:24,min:0,range:!0,values:[parseInt(a),parseInt(i)]}).slider("pips",{first:"pip",last:"pip"})})},window.get_day_night=o,g=function(e){var a,i;$(e).addClass("disabled"),$(e).addClass("loading"),i=$("#flat-slider-time-interval").slider("option","values"),a=$.ajax({url:"/change/day_night",method:"POST",data:{stop:parseInt(i[1].toString()+"00"),start:parseInt(i[0].toString()+"00"),ledbar:$(".field.ledbar > .ui.checkbox > input").prop("checked"),display:$(".field.display > .ui.checkbox > input").prop("checked"),generalleds:$(".field.generalleds > .ui.checkbox > input").prop("checked"),notification:$(".field.notification > .ui.checkbox > input").prop("checked")}}),a.done(function(a){return a=JSON.parse(a),$(e).removeClass("disabled"),$(e).removeClass("loading")})},window.modify_day_night=g,a=function(e,a){var i;console.log("target: "+e),console.log("host: "+a),i=$.ajax({url:"/update/slave/master",method:"POST",data:{target:e,slave:a}})},window.change_slave_host=a,c=function(){var e;e=$.ajax({url:"/get/manage",method:"POST"}),e.done(function(e){var i,n,t,l,o,s,d,r,c,u,p,g,v,m,f;for(e=JSON.parse(e),n="",s="<div class='item'> <div class='ui equal width grid'> <div class='column'> <a class='ui [[COLOR]] ribbon label' [[ADDITIONAL]]>[[MASTER]]</a> <span style='font-weight:bold'>[[NAME]]</span> </div> [[SLAVE]] <div class='column right aligned'> <div class='ui icon buttons'> <button class='ui button' onclick='window.location.href = \"/plant/[[LNAME]]/settings\"'> <i class='edit icon' /> </button> <button class='ui [[CHECKMARK_DISABLED]] button' onclick='manage_active_toggle(this, \"[[UUID]]\")'> <i class='[[CHECKMARK_ICON]] icon' /> </button> <button class='ui [[ERASE_DISABLED]] button' onclick='manage_purge(\"[[UUID]]\")'> <i class='[[ERASE_ICON]] icon' /> </button> </div> </div> </div> </div>",g="<div class='column'> My master is <div class='ui inline dropdown [[LNAME]] slave'> <div class='text'>[[HOST]]</div> <i class='dropdown icon' /> <div class='menu'> [[MASTERS]] </div> </div> </div>",r={},v={},t=0,o=e.length;t<o;t++)c=e[t],"master"===c.role?r[c.uuid]=c:v[c.uuid]=c;for(l in r)c=r[l],n+=s.replace("[[MASTER]]","Master").replace("[[NAME]]",_.capitalize(c.name)).replace("[[SLAVE]]","").replace("[[COLOR]]","red").replace("[[ADDITIONAL]]","").replace(/\[\[UUID\]\]/g,c.uuid).replace(/\[\[LNAME\]\]/g,c.name),c.localhost?n=n.replace("[[CHECKMARK_ICON]]","ban").replace("[[ERASE_ICON]]","ban").replace("[[CHECKMARK_DISABLED]]","disabled").replace("[[ERASE_DISABLED]]","disabled"):(f=c.active?"remove":"checkmark",n=n.replace("[[CHECKMARK_ICON]]",f).replace("[[ERASE_ICON]]","erase").replace("[[CHECKMARK_DISABLED]]","").replace("[[ERASE_DISABLED]]",""));for(l in v){c=v[l],i=s.replace("[[MASTER]]","Slave").replace(/\[\[NAME\]\]/,_.capitalize(c.name)).replace("[[COLOR]]","orange").replace("[[ADDITIONAL]]",m="style='padding-right:2em'"),p=g.replace("[[NAME]]",_.capitalize(c.name)).replace("[[HOST]]",_.capitalize(r[c.role].name)).replace(/\[\[LNAME\]\]/g,c.name),u="";for(l in r)d=r[l],u+="<div class='item' data-value='"+d.uuid+"'>"+_.capitalize(d.name)+"</div>";p=p.replace("[[MASTERS]]",u),n+=i.replace("[[SLAVE]]",p).replace("[[ERASE_ICON]]","erase").replace("[[CHECKMARK_ICON]]","ban").replace("[[CHECKMARK_DISABLED]]","disabled").replace("[[ERASE_DISABLED]]","").replace(/\[\[UUID\]\]/g,c.uuid)}$(".ui.relaxed.divided.list").html(n);for(l in v)c=v[l],$("."+c.name+".slave").dropdown({action:"activate",onChange:function(e,i,n){return console.log("testing stuff!"),a(e,c.role)}})})},window.init_manage=c,u=function(e,a){var i,n;i=$.ajax({url:"/update/plant/toggle",method:"POST",data:{uuid:a}}),n=$(e).children()[0],n.hasClass("checkmark")?n.removeClass("checkmark").addClass("remove"):n.removeClass("remove").addClass("checkmark"),i.done(function(e){window.location.href="/"})},window.manage_active_toggle=u,p=function(e){var a;a=$.ajax({url:"/update/plant/purge",method:"POST",data:{uuid:e}}),a.done(function(e){window.location.href="/"})},window.manage_purge=p}).call(this);