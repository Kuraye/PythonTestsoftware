import React from 'react';

import { %%NAAM%% } from './%%NAAM%%';

export default {
    title: '%%NAAM%%',
    component: %%NAAM%%
};

const Template = (args) => <%%NAAM%% {...args} />;

export const Primary = Template.bind({});
Primary.args = {
    label: '%%NAAM%%',
    info: '%%INFO%%',
    image: '%%IMAGE%%'
}