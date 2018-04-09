(function(){//+
	'use strict';		
					
	/**
	* Get control status
	* @param {Object} context
	* @param {boolean} isDefault - if true, get default (initial) control status; else - get current control status
	* @return {jQuery.fn.jplist.app.dto.StatusDTO}
	*/
	var getStatus = function(context, isDefault){
		
		var data
			,status = null
			,$button
			,cpage
			,itemsPerPage
			,lastStatus
			,isJumpToStart = false;
					
		//get active button  
		$button = context.$control.find('li[data-active]').eq(0);
		
		//if no active button -> get first button
		if($button.length <= 0){
			$button = context.$control.find('button').eq(0);
		}
		
		//get current page
		if(isDefault){
		
			//by default current page is 0
			cpage = 0;
		}
		else{
						
			//parse to number
			cpage = Number($button.attr('data-number')) || 0;
		}
				
		//if jumpToStart option is enabled and last rebuild action was not pagination -> jump to 0
		isJumpToStart = (context.$control.attr('data-jump-to-start') === 'true') || context.controlOptions.jumpToStart;
		
		if(isJumpToStart){
			
			lastStatus = context.history.getLastStatus();
			
			if(lastStatus && lastStatus.type !== 'pagination' && lastStatus.type !== 'views'){
				cpage = 0;
			}
		}
		
		//init items per page
		itemsPerPage = Number(context.$control.attr('data-items-per-page')) || 0;
		
		//create status related data
		data = new jQuery.fn.jplist.ui.controls.BootstrapPaginationDTO(cpage, itemsPerPage);		
			
		//create status
		status = new jQuery.fn.jplist.app.dto.StatusDTO(
			context.name
			,context.action
			,context.type
			,data
			,context.inStorage
			,context.inAnimation
			,context.isAnimateToTop
			,context.inDeepLinking
		);
		
		return status;			
	};
	
	/**
	* Get deep link
	* @param {Object} context
	* @return {string} deep link
	*/
	var getDeepLink = function(context){
		
		var deepLink = ''
			,status
			,isDefault = false;
		
		if(context.inDeepLinking){
		
			//get status
			status = getStatus(context, isDefault);
			
			if(status.data){
				
				if(jQuery.isNumeric(status.data.currentPage)){
					
					//init deep link
					deepLink = context.name + context.options.delimiter0 + 'currentPage=' + status.data.currentPage;
				}
				
				if(jQuery.isNumeric(status.data.number)){
					
					//init deep link
					deepLink = context.name + context.options.delimiter0 + 'number=' + status.data.number;
				}
			}
		}
		
		return deepLink;
	};
	
	/**
	* get status by deep link
	* @param {Object} context
	* @param {string} propName - deep link property name
	* @param {string} propValue - deep link property value
	* @return {jQuery.fn.jplist.app.dto.StatusDTO}
	*/
	var getStatusByDeepLink = function(context, propName, propValue){
		
		var isDefault = true
			,status = null;
		
		if(context.inDeepLinking){
		
			if(propName !== 'currentPage'){
				return null;
			}
			
			//get status
			status = getStatus(context, isDefault);
			
			if(status.data && (propName === 'currentPage')){
			
				//set current page
				status.data.currentPage = propValue;
			}
		}
		
		return status;
	};
			
	/**
	* Set control status
	* @param {Object} context
	* @param {jQuery.fn.jplist.app.dto.StatusDTO} status
	* @param {boolean} restoredFromStorage - is status restored from storage
	*/
	var setStatus = function(context, status, restoredFromStorage){
					
		if(status.data && status.data.paging){
					
			//build pager
			context.params.view.build(status.data.paging);
		}
	};
	
	/**
	* Init control events
	* @param {Object} context
	*/
	var initEvents = function(context){	
		
		/**
		* on pagination button click
		*/
		context.$control.on('click', 'li', function(){
			
			var currentPage
				,status = null;
			
			//get current page number			
			currentPage = Number(jQuery(this).attr('data-number')) || 0; 
			
			//get status
			status = getStatus(context, false);
			
			//update current page
			status.data.currentPage = currentPage;
						
			//send status event	
			context.observer.trigger(context.observer.events.statusChanged, [status]);
		});
	};
	
	/** 
	* Bootstrap Pagination Control
	* @constructor
	* @param {Object} context
	*/
	var Init = function(context){
			
		context.params = {			
			view: new jQuery.fn.jplist.ui.controls.BootstrapPaginationView(context.$control, context.controlOptions)
		};		
		
		//init events
		initEvents(context);
		
		return jQuery.extend(this, context);
	};
	
	/**
	* Get control status
	* @param {boolean} isDefault - if true, get default (initial) control status; else - get current control status
	* @return {jQuery.fn.jplist.app.dto.StatusDTO}
	*/
	Init.prototype.getStatus = function(isDefault){
		return getStatus(this, isDefault);
	};
	
	/**
	* Get Deep Link
	* @return {string} deep link
	*/
	Init.prototype.getDeepLink = function(){
		return getDeepLink(this);
	};
	
	/**
	* Get Paths by Deep Link
	* @param {string} propName - deep link property name
	* @param {string} propValue - deep link property value
	* @return {jQuery.fn.jplist.app.dto.StatusDTO}
	*/
	Init.prototype.getStatusByDeepLink = function(propName, propValue){
		return getStatusByDeepLink(this, propName, propValue);
	};
	
	/**
	* Set Status
	* @param {jQuery.fn.jplist.app.dto.StatusDTO} status
	* @param {boolean} restoredFromStorage - is status restored from storage
	*/
	Init.prototype.setStatus = function(status, restoredFromStorage){
		setStatus(this, status, restoredFromStorage);
	};
	
	/** 
	* Bootstrap Pagination Control
	* @constructor
	* @param {Object} context
	*/
	jQuery.fn.jplist.ui.controls.BootstrapPagination = function(context){
		return new Init(context);
	};	
	
	/**
	* static control registration
	*/
	jQuery.fn.jplist.controlTypes['boot-pagination'] = {
		className: 'BootstrapPagination'
		,options: {
		
			//paging
			range: 7
			,jumpToStart: false
			
			//arrows
			,prevArrow: '&lsaquo;'
			,nextArrow: '&rsaquo;'
			,firstArrow: '&laquo;'
			,lastArrow: '&raquo;'
		}
	};		
		
})();

