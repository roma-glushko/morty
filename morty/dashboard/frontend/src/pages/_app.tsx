import { AppProps } from 'next/app';
import { Layout, Breadcrumb } from 'antd';

import HeaderBar from '@/components/HeaderBar';

import 'antd/dist/antd.css';
import '@/styles/global.css';

const { Content, Footer } = Layout;

export default function MortyDashboard({ Component, pageProps }: AppProps) {
  return (
    <Layout className="layout">
      <HeaderBar />
      <Content style={{ padding: `0 50px` }}>
        <Breadcrumb style={{ margin: `16px 0` }}>
          <Breadcrumb.Item>Leaderboard</Breadcrumb.Item>
        </Breadcrumb>
        <div className="site-layout-content">
          <Component {...pageProps} />
        </div>
      </Content>
      <Footer style={{ textAlign: `center` }}>
        Made with ❤️ by Roman Glushko
      </Footer>
    </Layout>
  );
}
