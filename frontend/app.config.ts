export default defineAppConfig({
    ui: {
        formField: {
            error: 'text-md font-bold text-red-500' // Classes Tailwind CSS personnalisées
        },
        toast: {
            variants: {
                color: {
                    success: {
                        root: 'ring-green-700',
                        icon: 'text-white',
                        progress: 'bg-green-700'
                    },
                    error: {
                        root: 'ring-red-700',
                        icon: 'text-white',
                        progress: 'bg-red-700'
                    },
                    warning: {
                        root: 'ring-yellow-700',
                        icon: 'text-white',
                        progress: 'bg-yellow-700'
                    },
                    info: {
                        root: 'ring-blue-700',
                        icon: 'text-white',
                        progress: 'bg-blue-700'
                    }
                },
            },
        },
        toaster: {
            duration: 3000,
        }
    }
})
