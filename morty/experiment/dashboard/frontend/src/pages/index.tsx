import Head from 'next/head';

import { ExperimentTable } from '@/components/leaderboard/ExperimentTable';

import '@/styles/Leaderboard.module.css';

export default function LeaderboardPage(): JSX.Element {
  return (
    <div>
      <Head>
        <title>Leader Board - Morty Dashboard</title>
        <meta name="description" content="Morty Dashboard" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <ExperimentTable />
    </div>
  );
}
