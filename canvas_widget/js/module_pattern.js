http: //javascriptplayground.com/blog/2012/04/javascript-module-pattern/
http: //addyosmani.com/resources/essentialjsdesignpatterns/book/

var jspy = (function () {
    var _count = 0;
    var incrementCount = function () {
        _count++;
    };
    var resetCount = function () {
        _count = 0;
    };
    var getCount = function () {
        return _count;
    };
    return {
        add: incrementCount,
        reset: resetCount,
        get: getCount
    };
})();
