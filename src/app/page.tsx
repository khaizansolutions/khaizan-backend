import HeroSlider from '@/components/home/HeroSlider'
import CategoryGrid from '@/components/home/CategoryGrid'
import FeaturedProducts from '@/components/home/FeaturedProducts'

export default function Home() {
  return (
    <div>
      <HeroSlider />
      <CategoryGrid />
      <FeaturedProducts />
    </div>
  )
}