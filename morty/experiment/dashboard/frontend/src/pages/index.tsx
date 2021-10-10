import Head from 'next/head';

import styles from '@/styles/Home.module.css';
import { DatePicker } from 'antd';

import 'antd/dist/antd.css';


export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Leader Board - Morty Dashboard</title>
        <meta name="description" content="Morty Dashboard" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <DatePicker />
    </div>
  );
}
