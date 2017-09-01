import Ember from 'ember';

export default Ember.Controller.extend({
    queryParams: [
        'q',
        'departmentId',
    ],

    departmentId: "",

    isSelectedDepartment(department) {
        return department.get('id') == this.get('departmentId');
    },

    actions: {
        search() {
            let query = event.target.value;
            this.set('q', query);
        },

        searchButton(searchString) {
            this.set('q', searchString);
            if (!searchString) {
                Ember.$("#searchbox").focus();
            }
        },

        searchDepartment(departmentId) {
            this.set('departmentId', departmentId);
        }
    }
});
