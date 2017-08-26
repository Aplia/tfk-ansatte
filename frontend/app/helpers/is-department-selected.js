import Ember from 'ember';

export function isDepartmentSelected([department, id]) {
    return department.get('id') == id
}

export default Ember.Helper.helper(isDepartmentSelected);
