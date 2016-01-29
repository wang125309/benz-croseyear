var gulp = require('gulp');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var jshint = require('gulp-jshint');
var stylus = require('gulp-stylus');
var uglify = require('gulp-uglify');
var jade = require('gulp-jade');
var base64 = require('gulp-base64');
var css_minify = require('gulp-minify-css');
var browserify = require('gulp-browserify');

gulp.task('lint',function(){
    gulp.src('./static/js-modify/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('stylus',function(){
    gulp.src('./static/css-modify/*.styl')
        .pipe(stylus())
        .pipe(css_minify())
        .pipe(base64())
        .pipe(gulp.dest('./static/css'));
});

gulp.task('js',function(){
    gulp.src('./static/js-modify/*.js')
        .pipe(browserify())
        .pipe(gulp.dest('./static/js'))
        .pipe(uglify())
});

gulp.task('jade',function(){
    gulp.src('./template/jade/*.jade')
        .pipe(jade())
        .pipe(gulp.dest('./template/'))
});
