import { Layout, Menu } from 'antd';
import { ExperimentOutlined, TrophyOutlined } from '@ant-design/icons';

import styles from './HeaderBar.module.css';

const { Header } = Layout;

export default function HeaderBar() {
  return (
    <Header>
      <div className={styles.logo}>
        <ExperimentOutlined /> Morty
      </div>
      <Menu theme="dark" mode="horizontal">
        <Menu.Item key="leaderboard" icon={<TrophyOutlined />}>
          Leaderboard
        </Menu.Item>
      </Menu>
    </Header>
  );
}
