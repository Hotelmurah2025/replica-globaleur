import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

const resources = {
  en: {
    translation: {
      common: {
        loading: 'Loading...'
      },
      nav: {
        home: 'Home',
        destinations: 'Destinations',
        plans: 'Plans',
        contactUs: 'Contact Us',
        signIn: 'Sign In',
        signUp: 'Sign Up'
      },
      auth: {
        login: 'Login',
        register: 'Register',
        email: 'Email',
        password: 'Password',
        confirmPassword: 'Confirm Password'
      },
      hero: {
        title: 'Discover Your Next Adventure',
        subtitle: 'Find and plan your perfect trip with Cemelin'
      },
      home: {
        searchPlaceholder: 'Search destinations...',
        popularDestinations: 'Popular Destinations',
        exploreLocations: 'Explore trending locations around the world',
        planTrip: 'Plan Your Trip',
        createItinerary: 'Create custom itineraries for your journey',
        reviews: 'Travel Reviews',
        readExperiences: 'Read experiences from fellow travelers',
        exploreMore: 'Explore More'
      },
      destinations: {
        explore: 'Explore Destinations',
        viewDetails: 'View Details',
        activities: 'Recommended Activities',
        pageTitle: 'Explore Destinations',
        metaDescription: 'Discover amazing destinations across Indonesia. Plan your perfect trip with Cemelin Travel\'s curated collection of destinations.',
        searchLocation: 'Search location',
        reviews: 'Reviews'
      },
      plans: {
        title: 'Trip Planning',
        description: 'Plan your perfect trip with our interactive trip planner. Drag and drop activities to create your ideal itinerary.',
        availableActivities: 'Available Activities',
        dragActivities: 'Drag activities to plan your trip',
        day: 'Day {{number}}',
        addActivity: 'Add Activity',
        activityName: 'Activity Name',
        activityDuration: 'Duration',
        activityLocation: 'Location',
        activityNotes: 'Notes',
        activityAdded: 'Activity added to {{day}}',
        startPlanning: 'Start Planning',
        emptyPlan: 'Your trip plan is empty. Start by adding some activities!'
      },
      contact: {
        name: 'Name',
        subject: 'Subject',
        message: 'Message',
        send: 'Send Message',
        success: 'Message sent successfully!',
        error: 'Error sending message. Please try again.'
      },
      footer: {
        legal: 'Legal',
        terms: 'Terms of Service',
        privacy: 'Privacy Policy',
        followUs: 'Follow Us',
        rights: 'All rights reserved.'
      }
    }
  },
  id: {
    translation: {
      common: {
        loading: 'Memuat...'
      },
      nav: {
        home: 'Beranda',
        destinations: 'Destinasi',
        plans: 'Rencana',
        contactUs: 'Hubungi Kami',
        signIn: 'Masuk',
        signUp: 'Daftar'
      },
      auth: {
        login: 'Masuk',
        register: 'Daftar',
        email: 'Email',
        password: 'Kata Sandi',
        confirmPassword: 'Konfirmasi Kata Sandi'
      },
      hero: {
        title: 'Temukan Petualangan Berikutnya',
        subtitle: 'Temukan dan rencanakan perjalanan sempurna Anda dengan Cemelin'
      },
      home: {
        searchPlaceholder: 'Cari destinasi...',
        popularDestinations: 'Destinasi Populer',
        exploreLocations: 'Jelajahi lokasi trending di seluruh dunia',
        planTrip: 'Rencanakan Perjalanan',
        createItinerary: 'Buat rencana perjalanan kustom untuk perjalanan Anda',
        reviews: 'Ulasan Perjalanan',
        readExperiences: 'Baca pengalaman dari sesama pelancong',
        exploreMore: 'Jelajahi Lebih Lanjut'
      },
      destinations: {
        explore: 'Jelajahi Destinasi',
        viewDetails: 'Lihat Detail',
        activities: 'Aktivitas yang Direkomendasikan',
        pageTitle: 'Jelajahi Destinasi',
        metaDescription: 'Temukan destinasi menakjubkan di Indonesia. Rencanakan perjalanan sempurna Anda dengan koleksi destinasi pilihan Cemelin Travel.',
        searchLocation: 'Cari lokasi',
        reviews: 'Ulasan'
      },
      plans: {
        title: 'Perencanaan Perjalanan',
        availableActivities: 'Aktivitas Tersedia',
        dragActivities: 'Seret aktivitas untuk merencanakan perjalanan Anda',
        day: 'Hari'
      },
      contact: {
        name: 'Nama',
        subject: 'Subjek',
        message: 'Pesan',
        send: 'Kirim Pesan',
        success: 'Pesan berhasil dikirim!',
        error: 'Gagal mengirim pesan. Silakan coba lagi.'
      },
      footer: {
        legal: 'Legal',
        terms: 'Syarat dan Ketentuan',
        privacy: 'Kebijakan Privasi',
        followUs: 'Ikuti Kami',
        rights: 'Semua hak dilindungi.'
      }
    }
  }
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
