import { FunctionComponent } from 'react';
import { Table } from 'antd';

const columns = [
  {
    title: `Name`,
    dataIndex: `name`,
    filters: [
      {
        text: `Joe`,
        value: `Joe`,
      },
      {
        text: `Jim`,
        value: `Jim`,
      },
      {
        text: `Submenu`,
        value: `Submenu`,
        children: [
          {
            text: `Green`,
            value: `Green`,
          },
          {
            text: `Black`,
            value: `Black`,
          },
        ],
      },
    ],
    // specify the condition of filtering result
    // here is that finding the name started with `value`
    onFilter: (value: any, record: { name: string | any[]; }) => record.name.indexOf(value) === 0,
    sorter: (a: { name: string | any[] }, b: { name: string | any[] }) =>
      a.name.length - b.name.length,
    sortDirections: [`descend`],
  },
  {
    title: `Age`,
    dataIndex: `age`,
    defaultSortOrder: `descend`,
    sorter: (a: { age: number }, b: { age: number }) => a.age - b.age,
  },
  {
    title: `Address`,
    dataIndex: `address`,
    filters: [
      {
        text: `London`,
        value: `London`,
      },
      {
        text: `New York`,
        value: `New York`,
      },
    ],
    onFilter: (value: any, record: { address: string | any[] }) =>
      record.address.indexOf(value) === 0,
  },
];

const data = [
  {
    key: `1`,
    name: `John Brown`,
    age: 32,
    address: `New York No. 1 Lake Park`,
  },
  {
    key: `2`,
    name: `Jim Green`,
    age: 42,
    address: `London No. 1 Lake Park`,
  },
  {
    key: `3`,
    name: `Joe Black`,
    age: 32,
    address: `Sidney No. 1 Lake Park`,
  },
  {
    key: `4`,
    name: `Jim Red`,
    age: 32,
    address: `London No. 2 Lake Park`,
  },
];

function onChange(pagination: any, filters: any, sorter: any, extra: any) {
  console.log(`params`, pagination, filters, sorter, extra);
}

export const ExperimentTable: FunctionComponent = () => (
  <Table columns={columns} dataSource={data} onChange={onChange} />
);
