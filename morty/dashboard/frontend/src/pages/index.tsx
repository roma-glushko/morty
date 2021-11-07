import React from 'react'
import Head from 'next/head';

import { ExperimentTable } from '@/components/leaderboard/ExperimentTable';

import '@/styles/Leaderboard.module.css';

class LeaderboardPage extends React.Component {
  static async getInitialProps() {
    const res = await fetch(`https://api.github.com/repos/vercel/next.js`)
    const json = await res.json()
    return { stars: json.stargazers_count }
  }

  render() {
    return (
      <div>
        <Head>
          <title>Leader Board - Morty Dashboard</title>
          <meta name="description" content="Morty Dashboard" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <div>{this.props.stars}</div>
        <ExperimentTable />
      </div>
    );
  }
}

export default LeaderboardPage
