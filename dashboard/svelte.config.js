import { addBasePathToHrefAndSrc } from '@evidence-dev/sdk/build/svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: [
        {
            markup({ content, filename }) {
                // Intercept the compiled markdown files and ensure the missing SDK import is injected
                if (filename && filename.endsWith('.md')) {
                    if (content.includes('<script context="module">')) {
                        return {
                            code: content.replace(
                                '<script context="module">',
                                '<script context="module">\n    import { addBasePath } from \'@evidence-dev/sdk/utils/svelte\';'
                            )
                        };
                    }
                }
                return { code: content };
            }
        },
        addBasePathToHrefAndSrc
    ]
};

export default config;