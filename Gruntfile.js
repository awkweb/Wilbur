
module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        // compile scss
        sass: {
            dist: {
                options: {
                    style: 'compressed',
                    noCache: true
                },
                files: {
                    'wilbur/static/css/styles.css': 'wilbur/scss/styles.scss'
                }
            }
        },

        // autoprefix css
        autoprefixer: {
            dist: {
                files: {
                    'wilbur/static/css/styles.css': 'wilbur/static/css/styles.css'
                }
            }
        },

        // compile coffee
        //coffee : {
        //    compile: {
        //        files: {
        //            'path/to/result.js': 'path/to/source.coffee', // 1:1 compile
        //            'path/to/another.js': ['path/to/sources/*.coffee', 'path/to/more/*.coffee'] // compile and concat into single file
        //        }
        //    }
        //},

        // watch for changes
        watch: {
            css: {
                files: ['wilbur/scss/*.scss', 'wilbur/scss/partials/*.scss'], // scss files
                tasks: ['sass', 'autoprefixer'],
                options: {
                    interrupt: true,
                    spawn: false
                }
            }
            //js: {}
        }

    });

    // loads
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-coffee');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // tasks
    grunt.registerTask('default', ['sass', 'autoprefixer']); // add coffee
};
