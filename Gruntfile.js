module.exports = function(grunt) {

    // 1. All configuration goes here
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        // JavaScript
        concat: {
            // 2. Configuration for concatenating files goes here.
            dist: {
                src: [
                    //'js/vendors/*.js', // All JS in the libs folder
                    //'js/lib/*.js', // All JS in the libs folder
                    'main.js'  // This specific file
                ],
                dest: 'production.js',
                sourceMap: true
            }
        },
        uglify: {
            build: {
                src: 'production.js',
                dest: 'production.min.js',
                sourceMap: true
            }
        },
        // Style
        sass: {
            dist: {
                files: {
                    '.tmp-style.css': 'style.scss'
                }
            },
            options: {
                sourceMap: true,
                outputStyle: 'nested',
                imagePath: "../img"
            }
        },
        autoprefixer: {
            dist: {
                files: {
                    'compiled-style.css': '.tmp-style.css'
                },
                options: {
                    map: true
                }
            }
        },

        watch: {
            // options: {
            //     livereload: true,
            // },
            css: {
                files: ['*.scss'],
                tasks: ['sass', 'autoprefixer'],
                options: {
                    spawn: false,
                }
            },
            scripts: {
                files: ['*.js'],
                tasks: ['concat', 'uglify'],
                options: {
                    spawn: false,
                },
            }
        }

    });

    // 3. Where we tell Grunt we plan to use this plug-in.
    grunt.loadNpmTasks('grunt-browser-sync');
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-sass');

    // 4. Where we tell Grunt what to do when we type "grunt" into the terminal.
    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'autoprefixer', 'watch']);

};
