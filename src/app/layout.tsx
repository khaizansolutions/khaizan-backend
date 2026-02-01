import { Inter } from 'next/font/google'
import './globals.css'
import Header from '@/components/layout/Header'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import { QuoteProvider } from '@/context/QuoteContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Office Supplies Store',
  description: 'Your one-stop shop for all office supplies',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QuoteProvider>
          <Header />
          <Navbar />
          <main className="min-h-screen">
            {children}
          </main>
          <Footer />
        </QuoteProvider>
      </body>
    </html>
  )
}