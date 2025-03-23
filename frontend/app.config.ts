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
        },
        commandPalette: {
            slots: {
                root: 'flex flex-col min-h-400 min-w-0 divide-y divide-(--ui-border)',
                input: '[&>input]:h-16 text-3xl px-4',
                close: '',
                content: 'relative overflow-hidden flex flex-col',
                viewport: 'relative divide-y divide-(--ui-border) scroll-py-1 overflow-y-auto flex-1 focus:outline-none',
                group: 'p-2 isolate',
                empty: 'py-8 text-center text-lg text-(--ui-text-muted)',
                label: 'px-4 py-2 text-base font-semibold text-(--ui-text-highlighted)',
                item: 'group relative w-full flex items-center gap-4 px-4 py-3 text-lg select-none outline-none before:absolute before:z-[-1] before:inset-px before:rounded-[calc(var(--ui-radius)*1.5)] data-disabled:cursor-not-allowed data-disabled:opacity-75',
                itemLeadingIcon: 'shrink-0 size-6',
                itemLeadingAvatar: 'shrink-0',
                itemLeadingAvatarSize: 'sm',
                itemLeadingChip: 'shrink-0 size-6',
                itemLeadingChipSize: 'lg',
                itemTrailing: 'ms-auto inline-flex gap-2 items-center',
                itemTrailingIcon: 'shrink-0 size-6',
                itemTrailingHighlightedIcon: 'shrink-0 size-6 text-(--ui-text-dimmed) hidden group-data-highlighted:inline-flex',
                itemTrailingKbds: 'hidden lg:inline-flex items-center shrink-0 gap-1',
                itemTrailingKbdsSize: 'lg',
                itemLabel: 'truncate space-x-1 rtl:space-x-reverse text-(--ui-text-dimmed)',
                itemLabelBase: 'text-(--ui-text-highlighted) [&>mark]:text-(--ui-bg) [&>mark]:bg-(--ui-primary)',
                itemLabelPrefix: 'text-(--ui-text)',
                itemLabelSuffix: 'text-(--ui-text-dimmed) [&>mark]:text-(--ui-bg) [&>mark]:bg-(--ui-primary)'
            },
            variants: {
                active: {
                    true: {
                        item: 'text-(--ui-text-highlighted) before:bg-(--ui-bg-elevated)',
                        itemLeadingIcon: 'text-(--ui-text)'
                    },
                },
                loading: {
                    true: {
                        itemLeadingIcon: 'animate-spin'
                    }
                }
            }
        },
        navigationMenu: {
            variants: {
                color: {
                    primary: {
                        link: 'focus-visible:before:ring-orange-500',
                        childLink: 'focus-visible:outline-orange-500'
                    },
                },
            },
        },
    }
})
